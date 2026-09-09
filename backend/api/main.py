"""
FastAPI backend for PackSure Legal Metrology Compliance System
Integrates detection and OCR components for real-time processing
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import json
import shutil

# Import the legal metrology pipeline
import sys
from pathlib import Path

# Add project root to path for imports
# __file__ is backend/api/main.py, so we need to go up two levels to get project root
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "detection"))
sys.path.append(str(project_root / "processing"))
sys.path.append(str(project_root / "validation"))  # Add validation directory

# Import detection and OCR components
from detection.detector import YOLOv8Detector, detect_label_regions
from processing.ocr_engine import OCREngine, process_image_region
# Import validation component
from validation.validator import validate_fields

class LegalMetrologyPipeline:
    """
    Main pipeline that integrates detection and OCR components
    """

    def __init__(self,
                 detection_model_path: str = str(project_root / "detection" / "runs" / "detect" / "train2" / "weights" / "best.pt"),
                 ocr_lang: str = 'eng'):
        """
        Initialize the pipeline with detection and OCR components

        Args:
            detection_model_path: Path to YOLOv8 model file
            ocr_lang: Language for Tesseract OCR
        """
        # Initialize detection component
        self.detector = YOLOv8Detector(detection_model_path)

        # Initialize OCR component
        self.ocr_engine = OCREngine(lang=ocr_lang)

        # Class mapping from detection component
        self.class_names = {
            0: "MRP",
            1: "quantity",
            2: "manufacturer",
            3: "date"
        }

        print(f"Pipeline initialized:")
        print(f"  Detection model: {detection_model_path}")
        print(f"  OCR available: {hasattr(self.ocr_engine, 'lang')}")
        print(f"  OCR language: {ocr_lang}")

    def process_image(self, image: Union[str, np.ndarray]) -> List[Dict]:
        """
        Process an image through the complete pipeline: detection → OCR

        Args:
            image: Either file path (str) or numpy array (BGR format)

        Returns:
            List of dictionaries containing detection and OCR results:
            [
                {
                    "class": 0,
                    "bbox": [x1, y1, x2, y2],
                    "conf": 0.92,
                    "text": "extracted text",
                    "ocr_confidence": 0.87,
                    "field_name": "MRP"
                },
                ...
            ]
        """
        # Step 1: Run detection to find label regions
        detections = self.detector.detect_and_format(image)

        if not detections:
            print("No detections found in image")
            return []

        print(f"Detection found {len(detections)} regions")

        # Step 2: Load image if file path provided
        if isinstance(image, str):
            img_array = cv2.imread(image)
            if img_array is None:
                raise ValueError(f"Failed to load image from {image}")
        else:
            img_array = image

        # Step 3: Process each detection with OCR
        results = []

        for detection in detections:
            class_id = detection["class"]
            bbox = tuple(detection["bbox"])  # Convert list to tuple for OCR
            detection_conf = detection["conf"]

            # Get field name
            field_name = self.class_names.get(class_id, f"unknown_{class_id}")

            # Run OCR on the detected region
            ocr_result = self.ocr_engine.process_region(img_array, bbox=bbox)

            # Combine detection and OCR results
            combined_result = {
                "class": class_id,
                "bbox": detection["bbox"],
                "conf": detection_conf,
                "text": ocr_result["text"],
                "ocr_confidence": ocr_result["confidence"],
                "ocr_engine": ocr_result["engine"],
                "field_name": field_name
            }

            results.append(combined_result)

            print(f"  {field_name}: '{ocr_result['text']}' "
                  f"(det_conf={detection_conf:.2f}, ocr_conf={ocr_result['confidence']:.2f})")

        return results

    def process_and_format_for_validation(self, image: Union[str, np.ndarray]) -> List[Dict]:
        """
        Process image and format results specifically for validation component (TM3)

        Args:
            image: Either file path (str) or numpy array (BGR format)

        Returns:
            List of dictionaries in format expected by validation:
            [
                {"field": "MRP", "text": "₹199.00", "confidence": 0.95},
                ...
            ]
        """
        pipeline_results = self.process_image(image)

        validation_input = []
        for result in pipeline_results:
            validation_input.append({
                "field": result["field_name"],
                "text": result["text"],
                "confidence": result["ocr_confidence"]
            })

        return validation_input

def process_legal_metrology_image(image_path: str) -> List[Dict]:
    """
    Convenience function for simple usage

    Args:
        image_path: Path to image file

    Returns:
        List of detection + OCR results
    """
    pipeline = LegalMetrologyPipeline()
    return pipeline.process_image(image_path)

# Initialize FastAPI app
app = FastAPI(
    title="PackSure Legal Metrology API",
    description="API for detecting and validating legal metrology compliance on product labels",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance (initialized on startup)
pipeline: Optional[LegalMetrologyPipeline] = None

# In-memory storage for inspection states (for demo purposes)
# In production, this would be replaced with a proper database
inspection_store: Dict[str, Dict] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize the detection/OCR pipeline on startup"""
    global pipeline
    try:
        pipeline = LegalMetrologyPipeline()
        print("✅ Legal Metrology Pipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        # Don't fail startup - allow API to run with limited functionality
        pipeline = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "PackSure Legal Metrology Compliance API",
        "status": "operational",
        "pipeline_ready": pipeline is not None
    }

@app.post("/inspections")
async def upload_inspection_image(file: UploadFile = File(...)):
    """
    Upload and process a product inspection image
    Returns inspection ID and preliminary results
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Detection pipeline not available")

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read and process the image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Process image through pipeline
        results = pipeline.process_image(img)

        # Generate inspection ID
        import time
        inspection_id = f"insp_{int(time.time() * 1000)}"

        # Format results for frontend consumption
        bounding_boxes = []
        extracted_fields = []
        violations = []

        risk_score_value = 0

        # Process detection results
        for result in results:
            # Convert bbox from [x1, y1, x2, y2] to percentage format expected by frontend
            h, w = img.shape[:2]
            x1, y1, x2, y2 = result["bbox"]

            bbox_pct = {
                "id": f"box-{len(bounding_boxes)+1}",
                "label": result["field_name"],
                "x": round((x1 / w) * 100, 2),
                "y": round((y1 / h) * 100, 2),
                "width": round(((x2 - x1) / w) * 100, 2),
                "height": round(((y2 - y1) / h) * 100, 2),
                "status": "pass"  # Default - will be updated by validation
            }
            bounding_boxes.append(bbox_pct)

            # Format extracted field
            field_obj = {
                "parameter": result["field_name"],
                "detectedValue": result["text"] or "Not detected",
                "expectedValue": get_expected_value(result["field_name"]),
                "status": "pass"  # Default - will be updated by validation
            }
            extracted_fields.append(field_obj)

        # Prepare data for validation (format expected by validation.validator.py)
        validation_input = []
        for result in results:
            validation_input.append({
                "field": result["field_name"],
                "text": result["text"] or "",
                "confidence": result["ocr_confidence"]
            })

        # Run validation on extracted fields
        validation_results = validate_fields(validation_input) if validation_input else []

        # Process validation results to generate violations and update statuses
        violations = []
        risk_score_value = 0

        # Update bounding boxes and extracted fields with validation results
        for i, (bbox_pct, field_obj, validation_result) in enumerate(zip(bounding_boxes, extracted_fields, validation_results)):
            field_name = validation_result["field"]
            status = validation_result["status"]
            details = validation_result["details"]

            # Update status in bounding box and field object
            if status == "FAIL":
                bbox_pct["status"] = "flagged"
                field_obj["status"] = "flagged"

                # Generate violation based on field name and validation failure
                violation = generate_violation_for_field(field_name, details)
                if violation:
                    violations.append(violation)

            elif status == "UNCERTAIN":
                bbox_pct["status"] = "flagged"  # Treat uncertain as flagged for safety
                field_obj["status"] = "flagged"

                # Generate warning violation
                violation = generate_violation_for_field(field_name, f"Uncertain: {details}")
                if violation:
                    violations.append(violation)
            else:  # PASS
                bbox_pct["status"] = "pass"
                field_obj["status"] = "pass"

        # Calculate risk score based on violations
        risk_score_value = calculate_risk_score(violations)

        # Risk bands
        if risk_score_value <= 33:
            risk_band = "Low Risk - Minor Non-Compliance"
        elif risk_score_value <= 66:
            risk_band = "Medium Risk - Moderate Non-Compliance"
        else:
            risk_band = "High Risk - Significant Non-Compliance"

        # Store inspection state
        inspection_store[inspection_id] = {
            "inspectionId": inspection_id,
            "imageUrl": f"/inspections/{inspection_id}/image",  # Will serve the uploaded image
            "aiConfidence": 0.94,  # Placeholder - could be average of detection confidences
            "riskScore": {
                "value": min(risk_score_value, 100),
                "max": 100,
                "band": risk_band
            },
            "boundingBoxes": bounding_boxes,
            "extractedFields": extracted_fields,
            "violations": violations,
            "status": "completed",
            "timestamp": time.time()
        }

        # Return initial response
        return {
            "inspectionId": inspection_id,
            "imageUrl": inspection_store[inspection_id]["imageUrl"],
            "status": "processing"
        }

    except Exception as e:
        print(f"Error processing inspection: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/inspections/{inspection_id}/report")
async def get_compliance_report(inspection_id: str):
    """
    Get the full compliance report for an inspection
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    return inspection_store[inspection_id]

@app.get("/inspections/{inspection_id}/image")
async def get_inspection_image(inspection_id: str):
    """
    Serve the uploaded inspection image
    """
    # In a real implementation, we'd store the actual image data
    # For now, we'll return a placeholder or error
    raise HTTPException(status_code=501, detail="Image serving not implemented in this demo")

@app.post("/inspections/{inspection_id}/enhance")
async def enhance_image(
    inspection_id: str,
    operation: str = Form(...),
    params: str = Form("{}")
):
    """
    Apply enhancement operations to the inspection image
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    if not pipeline:
        raise HTTPException(status_code=503, detail="Detection pipeline not available")

    try:
        # Parse parameters
        import json
        params_dict = json.loads(params) if params else {}

        # In a real implementation, we would:
        # 1. Retrieve the original image
        # 2. Apply the enhancement operation (zoom, crop, deglare)
        # 3. Re-run detection/OCR on the enhanced image
        # 4. Update the inspection store with new results

        # For now, return mock success
        return {
            "success": True,
            "operation": operation,
            "message": f"Enhanced with {operation}",
            "inspectionId": inspection_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

@app.post("/inspections/{inspection_id}/sync")
async def sync_capture(inspection_id: str):
    """
    Simulate syncing with a connected camera/scanning device
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    return {
        "synced": True,
        "timestamp": inspection_store[inspection_id]["timestamp"]
    }

@app.get("/inspections/{inspection_id}/report/pdf")
async def generate_report_pdf(inspection_id: str):
    """
    Generate and return a PDF compliance report
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    # In a real implementation, we would generate an actual PDF
    # For now, return a placeholder
    raise HTTPException(status_code=501, detail="PDF generation not implemented in this demo")

@app.post("/inspections/{inspection_id}/escalate")
async def escalate_inspection(
    inspection_id: str,
    note: str = Form("")
):
    """
    Escalate a flagged inspection to a human compliance officer
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    # Update inspection state
    inspection_store[inspection_id]["escalated"] = True
    inspection_store[inspection_id]["escalationNote"] = note
    inspection_store[inspection_id]["escalatedAt"] = __import__('time').time()

    return {
        "escalated": True,
        "inspectionId": inspection_id,
        "message": f"Inspection {inspection_id} escalated to Senior Metrology Officer. Note: '{note or 'Manual review required'}'"
    }

@app.post("/inspections/{inspection_id}/confirm")
async def confirm_and_log(
    inspection_id: str,
    overrides: str = Form("{}")
):
    """
    Confirm the human-reviewed result and log it as final
    """
    if inspection_id not in inspection_store:
        raise HTTPException(status_code=404, detail="Inspection not found")

    try:
        # Parse overrides
        import json
        overrides_dict = json.loads(overrides) if overrides else {}

        # Update inspection state
        inspection_store[inspection_id]["confirmed"] = True
        inspection_store[inspection_id]["confirmationOverrides"] = overrides_dict
        inspection_store[inspection_id]["confirmedAt"] = __import__('time').time()

        return {
            "logged": True,
            "inspectionId": inspection_id,
            "timestamp": inspection_store[inspection_id]["confirmedAt"],
            "message": f"Inspection {inspection_id} confirmed and permanently logged to the digital audit trail."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Confirmation failed: {str(e)}")

def generate_violation_for_field(field_name: str, details: str) -> Optional[Dict]:
    """
    Generate a violation object based on field name and validation details
    """
    field_name_lower = field_name.lower().strip()

    # Define violation mappings based on Legal Metrology Rules
    violation_map = {
        "mrp": {
            "rule": "Rule 6(1)(e) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "MRP declaration does not contain the mandatory '(Inclusive of all taxes)' suffix or official ₹ currency symbol.",
            "severity": "Medium"
        },
        "quantity": {
            "rule": "Rule 6(1)(d) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Net quantity not expressed in standard SI units (g/kg/ml/L).",
            "severity": "Medium"
        },
        "manufacturer": {
            "rule": "Rule 6(1)(a) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Name and address of manufacturer/packer/importer not clearly visible or legible.",
            "severity": "Low"
        },
        "packer": {
            "rule": "Rule 6(1)(a) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Name and address of manufacturer/packer/importer not clearly visible or legible.",
            "severity": "Low"
        },
        "importer": {
            "rule": "Rule 6(1)(a) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Name and address of manufacturer/packer/importer not clearly visible or legible.",
            "severity": "Low"
        },
        "date": {
            "rule": "Rule 6(1)(c) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Date of manufacture/packing not clearly visible or not in valid format.",
            "severity": "Medium"
        },
        "mfg_date": {
            "rule": "Rule 6(1)(c) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Date of manufacture not clearly visible or not in valid format.",
            "severity": "Medium"
        },
        "exp_date": {
            "rule": "Rule 6(1)(c) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Expiry date not clearly visible or not in valid format.",
            "severity": "Medium"
        },
        "batch": {
            "rule": "Rule 6(1)(b) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Batch/lot number not clearly visible or missing.",
            "severity": "Low"
        },
        "consumer_care": {
            "rule": "Rule 6(1)(f) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Consumer care details (address, phone/email) not clearly visible or missing.",
            "severity": "Low"
        },
        "country_of_origin": {
            "rule": "Rule 6(1)(g) - Legal Metrology (Packaged Commodities) Rules, 2011",
            "description": "Country of origin not clearly visible or missing.",
            "severity": "Low"
        }
    }

    # Look for matching field name
    for key, violation in violation_map.items():
        if key in field_name_lower or field_name_lower in key:
            # Customize description based on validation details if provided
            if details and "invalid" in details.lower():
                return {
                    "rule": violation["rule"],
                    "description": details,
                    "severity": violation["severity"]
                }
            return violation.copy()

    # Generic violation for unknown fields
    return {
        "rule": "General Compliance Requirement",
        "description": f"Field '{field_name}' validation failed: {details}",
        "severity": "Low"
    }

def calculate_risk_score(violations: List[Dict]) -> int:
    """
    Calculate risk score based on violations and their severity
    """
    if not violations:
        return 0

    # Severity weights
    severity_weights = {
        "Low": 10,
        "Medium": 20,
        "High": 30
    }

    total_score = 0
    for violation in violations:
        severity = violation.get("severity", "Low")
        weight = severity_weights.get(severity, 10)
        total_score += weight

    # Cap at 100
    return min(total_score, 100)

def get_expected_value(field_name: str) -> str:
    """
    Get the expected value for a given field based on legal metrology standards
    """
    expected_values = {
        "MRP": "₹ XXX.XX (Incl. of all taxes)",
        "Net Quantity": "Standard SI unit (g / kg / ml)",
        "Mfg Date & Batch": "MM/YYYY format visible",
        "Consumer Care": "Name, address, tel/email of contact",
        "Barcode (EAN-13)": "Valid EAN-13 barcode"
    }

    return expected_values.get(field_name, "As per Legal Metrology Rules, 2011")

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
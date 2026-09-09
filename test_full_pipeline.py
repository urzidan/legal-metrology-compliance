"""
Test script to simulate the full pipeline with mock detections
to test the validation integration without needing a working detection model
"""
import sys
import os
from pathlib import Path
import numpy as np
import cv2

# Add project root to path
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.append(str(project_root))
sys.path.append(str(backend_path))
sys.path.append(str(backend_path / "api"))

def test_mock_pipeline():
    """Test the pipeline with mock detections to validate our validation integration"""
    print("Testing mock pipeline with validation integration...")

    try:
        # Change to backend directory to import properly
        backend_dir = str(project_root / "backend")
        if not os.path.exists(backend_dir):
            print(f"[ERROR] Backend directory not found: {backend_dir}")
            return False
        os.chdir(backend_dir)
        from api.main import LegalMetrologyPipeline
        print("[OK] Successfully imported LegalMetrologyPipeline")

        # Create a mock image (since detection isn't working)
        mock_img = np.zeros((480, 640, 3), dtype=np.uint8)
        mock_img[:] = (100, 150, 200)  # Light blue background

        # Add some text-like features to make it interesting
        cv2.putText(mock_img, 'TEST PRODUCT', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(mock_img, 'MRP: Rs. 199.00', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(mock_img, 'Net Qty: 500 g', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(mock_img, 'Mfg: ABC Foods', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(mock_img, 'Date: 03/24', (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        print(f"[OK] Created mock image: {mock_img.shape}")

        # Instead of using the broken detection, let's directly test our validation logic
        # by creating mock pipeline results that simulate what detection+OCR would return

        print("\n--- Simulating detection + OCR results ---")
        mock_pipeline_results = [
            {
                "class": 0,
                "bbox": [120, 180, 300, 210],  # [x1, y1, x2, y2] for MRP text
                "conf": 0.85,
                "text": "Rs. 199.00",
                "ocr_confidence": 0.90,
                "ocr_engine": "tesseract",
                "field_name": "MRP"
            },
            {
                "class": 1,
                "bbox": [120, 230, 250, 260],  # [x1, y1, x2, y2] for Quantity text
                "conf": 0.80,
                "text": "500 g",
                "ocr_confidence": 0.88,
                "ocr_engine": "tesseract",
                "field_name": "quantity"
            },
            {
                "class": 2,
                "bbox": [120, 280, 280, 310],  # [x1, y1, x2, y2] for Manufacturer text
                "conf": 0.75,
                "text": "ABC Foods",
                "ocr_confidence": 0.92,
                "ocr_engine": "tesseract",
                "field_name": "manufacturer"
            },
            {
                "class": 3,
                "bbox": [120, 330, 200, 350],  # [x1, y1, x2, y2] for Date text
                "conf": 0.70,
                "text": "03/24",
                "ocr_confidence": 0.85,
                "ocr_engine": "tesseract",
                "field_name": "date"
            }
        ]

        print(f"[OK] Created {len(mock_pipeline_results)} mock detection results")
        for i, result in enumerate(mock_pipeline_results):
            print(f"  {i+1}. {result['field_name']}: '{result['text']}' (det: {result['conf']:.2f}, ocr: {result['ocr_confidence']:.2f})")

        # Now test our validation logic directly (simulating what happens in the API)
        from validation.validator import validate_fields

        # Prepare data for validation (format expected by validation.validator.py)
        validation_input = []
        for result in mock_pipeline_results:
            validation_input.append({
                "field": result["field_name"],
                "text": result["text"] or "",
                "confidence": result["ocr_confidence"]
            })

        print(f"\n--- Running validation on {len(validation_input)} fields ---")
        validation_results = validate_fields(validation_input) if validation_input else []

        print("Validation Results:")
        for vr in validation_results:
            print(f"  {vr['field']}: '{vr.get('text', 'N/A')}' -> {vr['status']} - {vr['details']}")

        # Test our helper functions
        from api.main import generate_violation_for_field, calculate_risk_score, get_expected_value

        print(f"\n--- Testing helper functions ---")
        expected_mrp = get_expected_value("MRP")
        print(f"[OK] get_expected_value('MRP') = '{expected_mrp}'")

        violation = generate_violation_for_field("MRP", "Missing currency symbol")
        if violation and "rule" in violation:
            print(f"[OK] generate_violation_for_field works: {violation['rule']}")
        else:
            print("[ERROR] generate_violation_for_field failed")

        score = calculate_risk_score([{"severity": "Medium"}, {"severity": "Low"}])
        print(f"[OK] calculate_risk_score([Medium, Low]) = {score}")

        # Simulate what the API would do with these results
        print(f"\n--- Simulating API processing ---")

        # Convert detections to frontend format
        h, w = mock_img.shape[:2]
        bounding_boxes = []
        extracted_fields = []
        violations = []

        risk_score_value = 0

        # Process detection results (simulating the loop in upload_inspection_image)
        for i, (result, validation_result) in enumerate(zip(mock_pipeline_results, validation_results)):
            # Convert bbox from [x1, y1, x2, y2] to percentage format expected by frontend
            x1, y1, x2, y2 = result["bbox"]

            bbox_pct = {
                "id": f"box-{i+1}",
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

            # Update status based on validation
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
                    print(f"  [WARNING] Violation generated for {field_name}: {violation['rule']}")

            elif status == "UNCERTAIN":
                bbox_pct["status"] = "flagged"  # Treat uncertain as flagged for safety
                field_obj["status"] = "flagged"

                # Generate warning violation
                violation = generate_violation_for_field(field_name, f"Uncertain: {details}")
                if violation:
                    violations.append(violation)
                    print(f"  [WARNING] Uncertainty violation for {field_name}: {violation['rule']}")
            else:  # PASS
                bbox_pct["status"] = "pass"
                field_obj["status"] = "pass"
                print(f"  [OK] {field_name} PASSED validation")

        # Calculate risk score based on violations
        risk_score_value = calculate_risk_score(violations)

        # Risk bands
        if risk_score_value <= 33:
            risk_band = "Low Risk - Minor Non-Compliance"
        elif risk_score_value <= 66:
            risk_band = "Medium Risk - Moderate Non-Compliance"
        else:
            risk_band = "High Risk - Significant Non-Compliance"

        print(f"\n--- Final Results ---")
        print(f"Bounding Boxes: {len(bounding_boxes)}")
        print(f"Extracted Fields: {len(extracted_fields)}")
        print(f"Violations: {len(violations)}")
        print(f"Risk Score: {risk_score_value}/100 ({risk_band})")

        print("\nDetailed Results:")
        for i, (bbox, field) in enumerate(zip(bounding_boxes, extracted_fields)):
            status_emoji = "[OK]" if bbox["status"] == "pass" else "[WARNING]"
            print(f"  {status_emoji} {bbox['label']}: {field['detectedValue']} -> {bbox['status']}")

        if violations:
            print("\nViolations Found:")
            for v in violations:
                print(f"  [ERROR] [{v['severity']}] {v['rule']}")
                print(f"      {v['description']}")
        else:
            print("\n[SUCCESS] No violations found - Product appears compliant!")

        print(f"\n[TARGET] Pipeline simulation completed successfully!")
        print(f"[CHART] Risk Score: {risk_score_value}/100")
        return True

    except Exception as e:
        print(f"[ERROR] Mock pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Return to original directory
        os.chdir(project_root)

if __name__ == "__main__":
    print("=" * 70)
    print("PackSure Full Pipeline Simulation Test")
    print("(Testing validation integration with mock detections)")
    print("=" * 70)

    success = test_mock_pipeline()

    print("\n" + "=" * 70)
    if success:
        print("[SUCCESS] MOCK PIPELINE TEST PASSED!")
        print("[OK] Validation integration is working correctly")
        print("[LAUNCH] Ready for actual detection/OCR once model is fixed")
    else:
        print("[FAILURE] MOCK PIPELINE TEST FAILED")
        print("[TOOL] Please fix issues before proceeding")
    print("=" * 70)
"""
Integration Script for Legal Metrology Compliance
Links detection component (YOLOv8) with OCR component (Tesseract)
"""

import sys
import os
from typing import List, Dict, Union, Tuple
import numpy as np
import cv2

# Add project root to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..')
sys.path.append(root_dir)
sys.path.append(current_dir)

# Import detection component
from detection.detector import YOLOv8Detector, detect_label_regions

# Import OCR component
try:
    from processing.ocr_engine import OCREngine, process_image_region
    OCR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import OCREngine: {e}")
    print("Using mock OCR implementation")
    from processing.ocr_engine import MockOCREngine as OCREngine, process_image_region_mock as process_image_region
    OCR_AVAILABLE = False

class LegalMetrologyPipeline:
    """
    Main pipeline that integrates detection and OCR components
    """

    def __init__(self,
                 detection_model_path: str = "runs/detect/train2/weights/best.pt",
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
        print(f"  OCR available: {OCR_AVAILABLE}")
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

def main():
    """
    Main function for CLI usage
    """
    import argparse

    parser = argparse.ArgumentParser(description='Legal Metrology Compliance Pipeline')
    parser.add_argument('image', help='Path to input image')
    parser.add_argument('--model', default='runs/detect/train2/weights/best.pt',
                       help='Path to YOLOv8 model')
    parser.add_argument('--lang', default='eng',
                       help='Language for OCR')
    parser.add_argument('--format', choices=['pipeline', 'validation'],
                       default='pipeline',
                       help='Output format')

    args = parser.parse_args()

    try:
        # Initialize pipeline
        pipeline = LegalMetrologyPipeline(
            detection_model_path=args.model,
            ocr_lang=args.lang
        )

        # Process image
        if args.format == 'validation':
            results = pipeline.process_and_format_for_validation(args.image)
            print("\nValidation-ready output:")
        else:
            results = pipeline.process_image(args.image)
            print("\nPipeline output:")

        # Print results
        for i, result in enumerate(results):
            print(f"{i+1}. {result}")

        print(f"\nTotal regions processed: {len(results)}")

    except Exception as e:
        print(f"Error processing image: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
"""
Test integration between detection component (YOU) and OCR component (TM2 mock).
"""
import numpy as np
import cv2
import os
import sys

# Add the root and current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..')
sys.path.append(root_dir)
sys.path.append(current_dir)

# Import detection component
from detection.detector import YOLOv8Detector, detect_label_regions

# Import OCR component (we'll use the mock OCR engine for now)
from ocr_engine import MockOCREngine, process_image_region

def create_test_label_image():
    """Create a realistic test label image for demonstration"""
    # Create a white label background
    label = np.ones((300, 400, 3), dtype=np.uint8) * 255

    # Add some text-like regions (we'll draw rectangles to simulate text areas)
    # MRP region (top-left)
    cv2.rectangle(label, (20, 20), (180, 60), (200, 200, 200), -1)  # Light gray background
    cv2.putText(label, "MRP: ₹199.00", (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # Quantity region (below MRP)
    cv2.rectangle(label, (20, 70), (180, 110), (200, 200, 200), -1)
    cv2.putText(label, "Qty: 500 g", (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # Manufacturer region (below quantity)
    cv2.rectangle(label, (20, 120), (250, 160), (200, 200, 200), -1)
    cv2.putText(label, "Manuf: ABC Foods Ltd", (30, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Date region (bottom-left)
    cv2.rectangle(label, (20, 200), (150, 240), (200, 200, 200), -1)
    cv2.putText(label, "Exp: 03/24", (30, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Add some noise and imperfections to make it realistic
    noise = np.random.randint(-10, 10, label.shape, dtype=np.int16)
    label = np.clip(label.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return label

def main():
    print("=" * 70)
    print("Integration Test: Detection (YOU) -> OCR (TM2 mock)")
    print("=" * 70)

    # Step 1: Create test image
    print("\n1. Creating test label image...")
    test_image = create_test_label_image()
    image_path = "test_label_integration.jpg"
    cv2.imwrite(image_path, test_image)
    print(f"   Saved test image to: {image_path}")

    # Step 2: Run Detection Component (YOU)
    print("\n2. Running Detection Component (YOU)...")
    try:
        # Try to use the actual detection component
        detector = YOLOv8Detector("../detection/runs/detect/train2/weights/best.pt")
        detections = detector.detect_and_format(test_image)
        print(f"   Detector found {len(detections)} regions:")
        for i, det in enumerate(detections):
            class_name = ["MRP", "quantity", "manufacturer", "date"][det["class"]] if det["class"] < 4 else f"unknown({det['class']})"
            print(f"     {i+1}. Class {det['class']} ({class_name}): bbox={det['bbox']}, conf={det['conf']:.3f}")
    except Exception as e:
        print(f"   Error running actual detector: {e}")
        print("   Falling back to using detect_label_regions function...")
        detections = detect_label_regions(test_image, "../detection/runs/detect/train2/weights/best.pt")
        print(f"   Detector found {len(detections)} regions:")
        for i, det in enumerate(detections):
            class_name = ["MRP", "quantity", "manufacturer", "date"][det["class"]] if det["class"] < 4 else f"unknown({det['class']})"
            print(f"     {i+1}. Class {det['class']} ({class_name}): bbox={det['bbox']}, conf={det['conf']:.3f}")

    # Step 3: Run OCR Component (TM2 mock) on each detection
    print("\n3. Running OCR Component (TM2 mock) on each detection...")
    ocr_results = []
    engine = MockOCREngine()

    for i, det in enumerate(detections):
        class_id = det["class"]
        bbox = tuple(det["bbox"])  # Convert list to tuple
        detection_conf = det["conf"]

        # Process the region with OCR
        ocr_result = engine.process_region(test_image, bbox=bbox)

        # Combine detection and OCR results
        combined_result = {
            "detection": det,
            "ocr": ocr_result,
            "field_name": ["MRP", "quantity", "manufacturer", "date"][class_id] if class_id < 4 else f"unknown_{class_id}"
        }
        ocr_results.append(combined_result)

        print(f"   Region {i+1} ({combined_result['field_name']}):")
        print(f"     Detection: class={class_id}, conf={detection_conf:.3f}")
        print(f"     OCR: text='{ocr_result['text']}', conf={ocr_result['confidence']:.3f}, engine={ocr_result['engine']}")

    # Step 4: Show what would be passed to Validation Component (TM3)
    print("\n4. Prepared for Validation Component (TM3)...")
    validation_input = []
    for result in ocr_results:
        field_name = result["field_name"]
        validation_input.append({
            "field": field_name,
            "value": result["ocr"]["text"],
            "confidence": result["ocr"]["confidence"]
        })
        print(f"   {field_name}: '{validation_input[-1]['value']}' (conf={validation_input[-1]['confidence']:.2f})")

    # Step 5: Summary
    print("\n" + "=" * 70)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 70)
    print("\nFlow Summary:")
    print("  1. Input Image -> Detection Component (YOU)")
    print("     -> Returns: [{\"class\": 0, \"bbox\": [x1,y1,x2,y2], \"conf\": 0.92}, ...]")
    print("  2. Detections -> OCR Component (TM2)")
    print("     -> For each detection: crops region using bbox, applies Grayscale->CLAHE->Denoise->Tesseract")
    print("     -> Returns: {\"text\": \"extracted text\", \"confidence\": 0.XX, \"engine\": \"tesseract\"}")
    print("  3. OCR Results -> Validation Component (TM3)")
    print("     -> Receives: [{\"field\": \"MRP\", \"text\": \"Rs.199.00\", \"confidence\": 0.95}, ...]")
    print("\nKey Interfaces:")
    print("  Detection -> OCR: Bounding box coordinates [x1,y1,x2,y2]")
    print("  OCR -> Validation: Extracted text + confidence per field")
    print("\nNext Steps:")
    print("  - TM2 should implement their OCR processor in processing/ (replace MockOCREngine with real Tesseract implementation)")
    print("  - Update memory.md after integration testing")
    print("  - When TM2 is available, simply replace MockOCREngine with OCREngine in the above code")
    print("=" * 70)

    # Cleanup
    try:
        os.remove(image_path)
    except:
        pass

if __name__ == "__main__":
    main()

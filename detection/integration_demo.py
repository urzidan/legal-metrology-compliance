"""
Integration demo showing how the detection component interfaces with OCR (TM2)
This demonstrates the expected data flow:
Detection -> Cropping -> OCR -> Validation
"""

import os
import cv2
import json
from detector import YOLOv8Detector, detect_label_regions

def load_ground_truth(label_path):
    """Load YOLO format label file and convert to pixel coordinates"""
    detections = []
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 5:
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                # We need image width/height to convert to pixels - we'll assume 640x640
                # In real usage, we'd read the image dimensions
                img_w, img_h = 640, 640
                x1 = int((x_center - width/2) * img_w)
                y1 = int((y_center - height/2) * img_h)
                x2 = int((x_center + width/2) * img_w)
                y2 = int((y_center + height/2) * img_h)
                detections.append({
                    "class": class_id,
                    "bbox": [x1, y1, x2, y2],
                    "conf": 1.0  # Ground truth confidence
                })
    return detections

def mock_ocr(cropped_region):
    """Mock OCR that returns text based on average color (for demo)"""
    # In reality, this would call Tesseract or EasyOCR
    # For demo, we'll return a fixed string based on region brightness
    avg_brightness = cropped_region.mean()
    if avg_brightness > 200:
        return "₹ 199.00", 0.95  # MRP-like
    elif avg_brightness > 150:
        return "500 g", 0.90   # quantity-like
    elif avg_brightness > 100:
        return "ABC Foods Ltd", 0.85  # manufacturer-like
    else:
        return "03/24", 0.80    # date-like

def main():
    print("=" * 60)
    print("Legal Metrology Compliance: Detection -> OCR Integration Demo")
    print("=" * 60)

    # Use the synthetic dataset we generated
    base_dir = "synthetic_labels"
    image_dir = os.path.join(base_dir, "images")
    label_dir = os.path.join(base_dir, "labels")

    # Get first image-label pair
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.jpg')])
    if not image_files:
        print("No images found!")
        return

    img_file = image_files[0]
    label_file = os.path.splitext(img_file)[0] + ".txt"

    img_path = os.path.join(image_dir, img_file)
    label_path = os.path.join(label_dir, label_file)

    print(f"Image: {img_file}")
    print(f"Label: {label_file}")

    # Load image
    image = cv2.imread(img_path)
    if image is None:
        print("Failed to load image")
        return

    print(f"Image shape: {image.shape}")

    # Option 1: Use our detector (will return empty with pretrained model)
    print("\n--- Using YOLOv8 Detector (pretrained yolov8n.pt) ---")
    detector = YOLOv8Detector()  # Uses pretrained COCO model
    detections = detector.detect_and_format(image)
    print(f"Detector found {len(detections)} objects (likely 0 because model not trained for our classes)")

    # Option 2: Use ground truth as simulated detections (for demo)
    print("\n--- Using Ground Truth as Simulated Detections ---")
    gt_detections = load_ground_truth(label_path)
    print(f"Ground truth has {len(gt_detections)} label regions:")
    for i, det in enumerate(gt_detections):
        print(f"  {i+1}: Class {det['class']} ({['MRP','quantity','manufacturer','date'][det['class']]}), "
              f"bbox={det['bbox']}")

    # Simulate what TM2 (OCR) would do with these detections
    print("\n--- Simulating OCR Processing (TM2 Component) ---")
    ocr_results = []
    for det in gt_detections:
        class_id = det["class"]
        x1, y1, x2, y2 = det["bbox"]

        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.shape[1], x2)
        y2 = min(image.shape[0], y2)

        # Crop region
        if x2 > x1 and y2 > y1:
            cropped = image[y1:y2, x1:x2]
            text, confidence = mock_ocr(cropped)

            ocr_results.append({
                "field": ["MRP", "quantity", "manufacturer", "date"][class_id],
                "text": text,
                "confidence": confidence,
                "detection_bbox": det["bbox"],
                "detection_confidence": det["conf"]
            })
            print(f"  {['MRP','quantity','manufacturer','date'][class_id]}: "
                  f"OCR='{text}' (conf={confidence:.2f})")
        else:
            print(f"  Invalid bbox for class {class_id}: {det['bbox']}")

    # Show what would be passed to TM3 (Validation)
    print("\n--- Prepared for Validation (TM3 Component) ---")
    validation_input = []
    for result in ocr_results:
        validation_input.append({
            "field": result["field"],
            "value": result["text"],
            "confidence": result["confidence"]
        })

    print("Validation would receive:")
    for item in validation_input:
        print(f"  {item['field']}: '{item['value']}' (conf={item['confidence']:.2f})")

    # Save a visualization image with ground truth boxes drawn
    vis_image = image.copy()
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]  # BGR
    for det in gt_detections:
        class_id = det["class"]
        x1, y1, x2, y2 = det["bbox"]
        color = colors[class_id % len(colors)]
        label_text = ["MRP", "quantity", "manufacturer", "date"][class_id]
        cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(vis_image, label_text, (x1, y1-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    vis_path = "demo_visualization.jpg"
    cv2.imwrite(vis_path, vis_image)
    print(f"\nSaved visualization with ground truth boxes to: {vis_path}")

    print("\n" + "=" * 60)
    print("Demo complete! This shows the interface between components.")
    print("In a real system:")
    print("1. Detection component (YOU) provides bboxes and class IDs")
    print("2. OCR component (TM2) crops regions and extracts text")
    print("3. Validation component (TM3) checks text against rules")
    print("4. Integration component (TM6) orchestrates the flow")
    print("=" * 60)

if __name__ == "__main__":
    main()
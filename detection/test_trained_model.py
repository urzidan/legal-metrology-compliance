"""
Test the trained YOLOv8 model on synthetic data
"""

from detector import YOLOv8Detector
import os

def test_trained_model():
    # Path to the best model from training
    model_path = r'synthetic_labels\runs\detect\train\weights\best.pt'
    # Use raw string to avoid issues with backslashes on Windows
    # Alternatively, use forward slashes or os.path.join
    model_path = os.path.join('synthetic_labels', 'runs', 'detect', 'train', 'weights', 'best.pt')

    print(f"Loading trained model from: {model_path}")
    detector = YOLOv8Detector(model_path=model_path)

    # Test on a few images
    image_dir = os.path.join('synthetic_labels', 'images')
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.jpg')])[:5]

    print(f"Testing on {len(image_files)} images from {image_dir}")
    total_detections = 0
    for img_file in image_files:
        img_path = os.path.join(image_dir, img_file)
        detections = detector.detect_and_format(img_path)
        total_detections += len(detections)
        print(f"  {img_file}: {len(detections)} detections")
        for d in detections[:2]:  # Show first 2 detections per image
            print(f"    Class {d['class']}: bbox={d['bbox']}, conf={d['conf']:.3f}")

    print(f"\nTotal detections across {len(image_files)} images: {total_detections}")
    if total_detections > 0:
        print("✅ Model is detecting objects!")
    else:
        print("⚠️  No detections - may need more training or check labels.")

if __name__ == "__main__":
    test_trained_model()
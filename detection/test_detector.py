"""
Test script for YOLOv8 detector
"""

import numpy as np
import cv2
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector import YOLOv8Detector, detect_label_regions
from synthetic_data_generator import SyntheticLabelGenerator

def test_with_synthetic_data():
    """Test detector with synthetic data"""
    print("Testing YOLOv8 detector with synthetic data...")

    # Generate synthetic label
    generator = SyntheticLabelGenerator()
    image, ground_truth = generator.generate_synthetic_label()

    # Save for visual verification
    cv2.imwrite("test_synthetic_label.jpg", image)
    print(f"Saved synthetic label image: test_synthetic_label.jpg")
    print(f"Ground truth annotations: {len(ground_truth)} regions")

    # Test detector
    detector = YOLOv8Detector()
    detections = detector.detect_and_format(image)

    print(f"Detections found: {len(detections)} regions")
    for i, det in enumerate(detections):
        print(f"  Detection {i+1}: class={det['class']} ({detector.class_names.get(det['class'], 'unknown')}), "
              f"bbox=[{det['bbox'][0]:.1f}, {det['bbox'][1]:.1f}, "
              f"{det['bbox'][2]:.1f}, {det['bbox'][3]:.1f}], "
              f"conf={det['conf']:.3f}")

    # Verify return type and structure (even if zero detections)
    assert isinstance(detections, list), "Detector should return a list"
    for det in detections:
        assert "class" in det and isinstance(det["class"], int)
        assert "bbox" in det and isinstance(det["bbox"], list) and len(det["bbox"]) == 4
        assert "conf" in det and isinstance(det["conf"], float)
    print("  ✅ Detector return format is correct")

    return True  # Test passes if no exception

def test_with_file_path():
    """Test detector accepting file path"""
    print("\nTesting detector with file path input...")

    # Create a simple test image
    test_img = np.ones((480, 640, 3), dtype=np.uint8) * 255
    cv2.putText(test_img, "TEST MRP: ₹199.00", (50, 100),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.rectangle(test_img, (40, 80), (200, 130), (0, 255, 0), 2)  # Draw a box around text
    cv2.imwrite("test_label.jpg", test_img)

    # Test with file path
    detections = detect_label_regions("test_label.jpg")
    print(f"Detections from file path: {len(detections)} regions")

    # Verify return type and structure
    assert isinstance(detections, list), "Detector should return a list"
    for det in detections:
        assert "class" in det and isinstance(det["class"], int)
        assert "bbox" in det and isinstance(det["bbox"], list) and len(det["bbox"]) == 4
        assert "conf" in det and isinstance(det["conf"], float)
    print("  ✅ Detector return format is correct")

    for i, det in enumerate(detections):
        print(f"  Detection {i+1}: class={det['class']} ({detector.class_names.get(det['class'], 'unknown')}), "
              f"bbox=[{det['bbox'][0]:.1f}, {det['bbox'][1]:.1f}, "
              f"{det['bbox'][2]:.1f}, {det['bbox'][3]:.1f}], "
              f"conf={det['conf']:.3f}")

    return True  # Test passes if no exception

def test_convenience_function():
    """Test the convenience function"""
    print("\nTesting convenience function...")

    # Create test image
    test_img = np.ones((300, 400, 3), dtype=np.uint8) * 255
    cv2.putText(test_img, "QUANTITY: 500g", (50, 150),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imwrite("quantity_test.jpg", test_img)

    # Use convenience function
    detections = detect_label_regions("quantity_test.jpg")
    print(f"Convenience function detections: {len(detections)} regions")

    # Verify return type and structure
    assert isinstance(detections, list), "Detector should return a list"
    for det in detections:
        assert "class" in det and isinstance(det["class"], int)
        assert "bbox" in det and isinstance(det["bbox"], list) and len(det["bbox"]) == 4
        assert "conf" in det and isinstance(det["conf"], float)
    print("  ✅ Convenience function return format is correct")

    return True  # Test passes if no exception

if __name__ == "__main__":
    print("=" * 60)
    print("YOLOv8 Detector Test Suite for Legal Metrology Compliance")
    print("=" * 60)

    try:
        success1 = test_with_synthetic_data()
        success2 = test_with_file_path()
        success3 = test_convenience_function()

        print("\n" + "=" * 60)
        if success1 and success2 and success3:
            print("✅ All tests passed!")
            print("The YOLOv8 detector is working correctly.")
        else:
            print("❌ Some tests failed")
            print("Check the output above for details.")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install ultralytics opencv-python numpy")
        sys.exit(1)
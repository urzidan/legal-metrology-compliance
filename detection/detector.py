"""
YOLOv8 Detector for Legal Metrology Compliance
Detects label regions: MRP, quantity, manufacturer, date
"""

from ultralytics import YOLO
import numpy as np
from typing import Union, List, Dict

class YOLOv8Detector:
    def __init__(self, model_path: str = "runs/detect/train2/weights/best.pt"):
        """
        Initialize YOLOv8 detector

        Args:
            model_path: Path to YOLOv8 model file (default: runs/detect/train2/weights/best.pt for trained model)
        """
        self.model = YOLO(model_path)
        # Class mapping: 0=MRP, 1=quantity, 2=manufacturer, 3=date
        self.class_names = {
            0: "MRP",
            1: "quantity",
            2: "manufacturer",
            3: "date"
        }

    def detect(self, image: Union[str, np.ndarray]) -> List[Dict]:
        """
        Detect label regions in an image

        Args:
            image: Either file path (str) or numpy array

        Returns:
            List of detections in format:
            [{"class": 0, "bbox": [x1,y1,x2,y2], "conf": 0.92}, ...]
        """
        # Run inference
        results = self.model(image)

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Extract box coordinates and confidence
                    x1, y1, x2, y2 = box.xyxy[0].tolist()  # Bounding box
                    confidence = box.conf[0].item()        # Confidence score
                    class_id = int(box.cls[0].item())      # Class ID

                    detections.append({
                        "class": class_id,
                        "bbox": [x1, y1, x2, y2],
                        "conf": confidence
                    })

        return detections

    def detect_and_format(self, image: Union[str, np.ndarray]) -> List[Dict]:
        """
        Detect and return in the exact format specified in requirements

        Returns format: [{"class": 0, "bbox": [x1,y1,x2,y2], "conf": 0.92}, ...]
        """
        return self.detect(image)

# Convenience function for simple usage
def detect_label_regions(image: Union[str, np.ndarray],
                        model_path: str = "runs/detect/train2/weights/best.pt") -> List[Dict]:
    """
    Simple function to detect label regions

    Args:
        image: File path or numpy array
        model_path: Path to YOLOv8 model

    Returns:
        List of detections in required format
    """
    detector = YOLOv8Detector(model_path)
    return detector.detect_and_format(image)
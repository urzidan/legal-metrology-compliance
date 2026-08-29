"""
Synthetic Data Generator for YOLOv8 Training
Generates synthetic label images for training the detection model
"""

import numpy as np
import cv2
from typing import Tuple, List, Dict
import os
import random
import json

print("Starting synthetic data generation...")

class SyntheticLabelGenerator:
    def __init__(self, image_size: Tuple[int, int] = (640, 640)):
        self.image_size = image_size
        self.class_names = ["MRP", "quantity", "manufacturer", "date"]

    def generate_synthetic_label(self,
                               num_regions: int = 4,
                               include_text: bool = True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Generate a synthetic label image with bounding box annotations

        Args:
            num_regions: Number of label regions to generate
            include_text: Whether to render text in regions

        Returns:
            Tuple of (image, annotations) where:
            - image: Synthetic label as numpy array
            - annotations: List of dicts with class, bbox coordinates
        """
        # Create blank label background (white)
        image = np.ones((*self.image_size, 3), dtype=np.uint8) * 255

        annotations = []
        h, w = self.image_size

        # Generate random regions for label fields
        for i in range(min(num_regions, len(self.class_names))):
            # Random bounding box within image bounds
            x1 = random.randint(0, w//2)
            y1 = random.randint(0, h//2)
            x2 = random.randint(x1+50, min(x1+200, w))
            y2 = random.randint(y1+20, min(y1+50, h))

            # Ensure box is within bounds
            x1, x2 = max(0, x1), min(w, x2)
            y1, y2 = max(0, y1), min(h, y2)

            # Draw rectangle (for visualization)
            color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # Add text label if requested
            if include_text:
                label_text = self.class_names[i]
                cv2.putText(image, label_text, (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            annotations.append({
                "class": i,
                "bbox": [float(x1), float(y1), float(x2), float(y2)],
                "conf": 1.0  # Synthetic data has perfect confidence
            })

        return image, annotations

    def generate_dataset(self,
                        num_samples: int = 100,
                        output_dir: str = "synthetic_dataset"):
        """
        Generate a complete synthetic dataset

        Args:
            num_samples: Number of synthetic images to generate
            output_dir: Directory to save dataset
        """
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)

        dataset_info = []

        for i in range(num_samples):
            # Generate synthetic label
            image, annotations = self.generate_synthetic_label()

            # Save image
            img_path = os.path.join(output_dir, "images", f"synthetic_{i:04d}.jpg")
            cv2.imwrite(img_path, image)

            # Save YOLO format labels
            label_path = os.path.join(output_dir, "labels", f"synthetic_{i:04d}.txt")
            with open(label_path, 'w') as f:
                for ann in annotations:
                    # Convert to YOLO format: class x_center y_center width height (normalized)
                    x1, y1, x2, y2 = ann["bbox"]
                    x_center = (x1 + x2) / 2 / self.image_size[0]
                    y_center = (y1 + y2) / 2 / self.image_size[1]
                    width = (x2 - x1) / self.image_size[0]
                    height = (y2 - y1) / self.image_size[1]

                    f.write(f"{ann['class']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

            dataset_info.append({
                "image_path": img_path,
                "label_path": label_path,
                "annotations": annotations
            })

        # Save dataset info
        with open(os.path.join(output_dir, "dataset_info.json"), 'w') as f:
            json.dump(dataset_info, f, indent=2)

        print(f"Generated {num_samples} synthetic samples in {output_dir}")

# Convenience function
def generate_synthetic_label_data(num_samples: int = 50,
                                output_dir: str = "synthetic_labels") -> str:
    """
    Generate synthetic label data for training

    Args:
        num_samples: Number of samples to generate
        output_dir: Output directory

    Returns:
        Path to generated dataset
    """
    generator = SyntheticLabelGenerator()
    generator.generate_dataset(num_samples, output_dir)
    return output_dir

if __name__ == "__main__":
    # Generate synthetic data when script is run directly
    generate_synthetic_label_data()
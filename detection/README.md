# Detection Component

This component handles the detection of label regions (MRP, quantity, manufacturer, date) using YOLOv8.

## Files

- `detector.py` - Main YOLOv8 detector implementation
- `synthetic_data_generator.py` - Generates synthetic label data for training/testing
- `test_detector.py` - Unit tests for the detector
- `integration_demo.py` - Demonstrates interface with OCR component (TM2)
- `test_trained_model.py` - Tests a trained model (after running training)

## Usage

### Basic Detection
```python
from detector import detect_label_regions
detections = detect_label_regions("path/to/image.jpg")
# Returns: [{"class": 0, "bbox": [x1,y1,x2,y2], "conf": 0.92}, ...]
# Class mapping: 0=MRP, 1=quantity, 2=manufacturer, 3=date
```

### Generate Synthetic Data
```bash
python synthetic_data_generator.py
# Creates synthetic_dataset/ with images and YOLO-format labels
```

### Train a Custom Model
```bash
# First generate dataset and create data.yaml (see synthetic_data_generator.py)
yolo detect train data=data.yaml model=yolov8n.pt epochs=20 imgsz=640
```

### Run Tests
```bash
python test_detector.py
```

## Integration with TM2 (OCR Component)

The detection component provides TM2 with:
- Input: Image (file path or numpy array)
- Output: List of detections in the format above

TM2 should:
1. Receive detection list
2. For each detection, crop region: `cropped = image[y1:y2, x1:x2]`
3. Run OCR on each cropped region
4. Return text + confidence for each region

See `integration_demo.py` for a full example of this flow.
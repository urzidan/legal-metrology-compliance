# OCR Processing Component (TM2)

This component handles text extraction from image regions using Tesseract OCR with preprocessing pipeline.

## Files

- `ocr_engine.py` - Main OCR implementation
- `test_ocr.py` - Unit tests for the OCR processor
- `integration_demo.py` - Demonstrates interface with detection component (YOU)

## Usage

### Basic OCR Processing
```python
from ocr_engine import process_image_region
result = process_image_region("path/to/image.jpg")
# Returns: {"text": "₹ 199.00", "confidence": 0.87, "engine": "tesseract"}

# With bounding box cropping
result = process_image_region("path/to/image.jpg", bbox=(x1, y1, x2, y2))
```

### OCR Engine Class
```python
from ocr_engine import OCREngine

engine = OCREngine(lang='eng')  # Initialize with language
result = engine.process_region(image_array, bbox=(x1, y1, x2, y2))
```

## Processing Pipeline

The OCR component applies the following preprocessing steps before Tesseract:
1. **Grayscale Conversion** - Convert BGR image to grayscale
2. **CLAHE** - Contrast Limited Adaptive Histogram Equalization (clipLimit=2.0, tileGridSize=(8,8))
3. **Denoising** - Fast Non-Local Means Denoising (h=10)
4. **Tesseract OCR** - Extract text with confidence scores

## Return Format

Always returns a dictionary with:
- `"text"`: Extracted text string (empty string if no text found or on error)
- `"confidence"`: Confidence score (0.0 to 1.0)
- `"engine"`: OCR engine used ("tesseract" or "mock-tesseract" for testing)

On failure (exception or no readable text):
```python
{"text": "", "confidence": 0.0, "engine": "tesseract"}
```

## Integration with Detection Component (YOU)

The detection component should provide:
- Input: Image (file path or numpy array)
- Output: `[{"class": 0, "bbox": [x1,y1,x2,y2], "conf": 0.92}, ...]`
  - Class mapping: 0=MRP, 1=quantity, 2=manufacturer, 3=date

TM2's OCR component expects:
- Input: Image + list of detections from above
- For each detection:
  1. Crop region using bbox: `cropped = image[y1:y2, x1:x2]`
  2. Apply OCR pipeline to cropped region
  3. Return: `{"text": "...", "confidence": 0.XX, "engine": "tesseract"}`

The combined output for TM3 (Validation) should be:
`[{"field": "MRP", "text": "₹199.00", "confidence": 0.95}, ...]`

## Dependencies

- `pytesseract>=0.3.10`
- `Pillow>=10.0.0`
- `opencv-python>=4.8.0` (used in preprocessing)

Note: Tesseract OCR engine must be installed separately on the system:
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`

## Testing

Run the test suite:
```bash
cd processing
python test_ocr.py
```
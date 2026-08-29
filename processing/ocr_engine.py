"""
OCR Processor for Legal Metrology Compliance
Extracts text from image regions using Tesseract with preprocessing pipeline
"""

import cv2
import numpy as np
import pytesseract
from typing import Union, Dict, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCREngine:
    def __init__(self, lang: str = 'eng'):
        """
        Initialize OCR engine with Tesseract

        Args:
            lang: Language for Tesseract (default: 'eng')
        """
        self.lang = lang
        # Check if tesseract is available
        try:
            pytesseract.get_tesseract_version()
            logger.info(f"Tesseract version: {pytesseract.get_tesseract_version()}")
        except Exception as e:
            logger.warning(f"Tesseract not found or not accessible: {e}")
            logger.warning("OCR will use mock implementation for demonstration")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing pipeline: Grayscale → CLAHE → Denoise

        Args:
            image: Input image (BGR or grayscale)

        Returns:
            Preprocessed grayscale image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)

        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)

        return denoised

    def extract_text(self, image: np.ndarray) -> Dict[str, Union[str, float]]:
        """
        Extract text from preprocessed image using Tesseract

        Args:
            image: Preprocessed grayscale image

        Returns:
            Dictionary with text, confidence, and engine info
        """
        try:
            # Use Tesseract to get text and confidence data
            # We'll use image_to_data to get confidence scores
            data = pytesseract.image_to_data(
                image,
                lang=self.lang,
                output_type=pytesseract.Output.DICT,
                config='--psm 8'  # Treat image as single word line
            )

            # Extract text and calculate average confidence
            text_parts = []
            confidences = []

            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                conf = int(data['conf'][i])

                if text and conf > 0:  # Filter out empty text and negative confidence
                    text_parts.append(text)
                    confidences.append(conf)

            # Combine text parts
            full_text = ' '.join(text_parts)

            # Calculate average confidence if we have valid detections
            if confidences:
                avg_confidence = sum(confidences) / len(confidences) / 100.0  # Convert to 0-1 scale
            else:
                avg_confidence = 0.0
                full_text = ""

            return {
                "text": full_text,
                "confidence": avg_confidence,
                "engine": "tesseract"
            }

        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "engine": "tesseract"
            }

    def process_region(self, image: np.ndarray, bbox: Tuple[int, int, int, int] = None) -> Dict[str, Union[str, float]]:
        """
        Process an image region: optionally crop to bbox, then apply full OCR pipeline

        Args:
            image: Input image (BGR format)
            bbox: Optional bounding box (x1, y1, x2, y2) to crop. If None, use full image.

        Returns:
            Dictionary with text, confidence, and engine info
        """
        try:
            # Crop to bbox if provided
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                # Ensure coordinates are within image bounds
                h, w = image.shape[:2]
                x1 = max(0, min(x1, w))
                y1 = max(0, min(y1, h))
                x2 = max(x1, min(x2, w))
                y2 = max(y1, min(y2, h))

                if x2 <= x1 or y2 <= y1:
                    logger.warning(f"Invalid bbox {bbox} after clamping to image size {w}x{h}")
                    return {"text": "", "confidence": 0.0, "engine": "tesseract"}

                cropped = image[y1:y2, x1:x2]
            else:
                cropped = image

            # Apply preprocessing pipeline
            preprocessed = self.preprocess_image(cropped)

            # Extract text
            result = self.extract_text(preprocessed)

            logger.debug(f"OCR result: {result}")
            return result

        except Exception as e:
            logger.error(f"Region processing failed: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "engine": "tesseract"
            }

# Convenience function for simple usage
def process_image_region(image: Union[str, np.ndarray],
                        bbox: Tuple[int, int, int, int] = None,
                        lang: str = 'eng') -> Dict[str, Union[str, float]]:
    """
    Simple function to process an image region with OCR

    Args:
        image: File path (str) or numpy array (BGR format)
        bbox: Optional bounding box (x1, y1, x2, y2) to crop
        lang: Language for Tesseract

    Returns:
        Dictionary with text, confidence, and engine info
    """
    engine = OCREngine(lang=lang)

    # Load image if file path provided
    if isinstance(image, str):
        img_array = cv2.imread(image)
        if img_array is None:
            logger.error(f"Failed to load image from {image}")
            return {"text": "", "confidence": 0.0, "engine": "tesseract"}
    else:
        img_array = image

    return engine.process_region(img_array, bbox)

# Mock implementation for when Tesseract is not available
class MockOCREngine:
    """Mock OCR engine for testing when Tesseract is not installed"""

    def __init__(self, lang: str = 'eng'):
        self.lang = lang
        logger.warning("Using Mock OCR Engine - Tesseract not available")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Simple grayscale conversion for mock"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image.copy()

    def extract_text(self, image: np.ndarray) -> Dict[str, Union[str, float]]:
        """Mock extraction that returns placeholder text based on image properties"""
        # Calculate some basic image properties to return different mock text
        mean_val = np.mean(image)
        std_val = np.std(image)

        # Return different mock text based on brightness/variance
        if mean_val > 200:
            text = "₹ 199.00"
            confidence = 0.95
        elif mean_val > 150:
            text = "500 g"
            confidence = 0.90
        elif mean_val > 100:
            text = "ABC Foods Ltd"
            confidence = 0.85
        else:
            text = "03/24"
            confidence = 0.80

        # Add some variance to confidence based on image properties
        confidence = max(0.1, min(0.99, confidence + (std_val - 50) / 500.0))

        return {
            "text": text,
            "confidence": confidence,
            "engine": "mock-tesseract"
        }

    def process_region(self, image: np.ndarray, bbox: Tuple[int, int, int, int] = None) -> Dict[str, Union[str, float]]:
        """Process region with mock OCR"""
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            h, w = image.shape[:2]
            x1 = max(0, min(x1, w))
            y1 = max(0, min(y1, h))
            x2 = max(x1, min(x2, w))
            y2 = max(y1, min(y2, h))

            if x2 <= x1 or y2 <= y1:
                return {"text": "", "confidence": 0.0, "engine": "mock-tesseract"}

            cropped = image[y1:y2, x1:x2]
        else:
            cropped = image

        preprocessed = self.preprocess_image(cropped)
        return self.extract_text(preprocessed)

def process_image_region_mock(image: Union[str, np.ndarray],
                             bbox: Tuple[int, int, int, int] = None,
                             lang: str = 'eng') -> Dict[str, Union[str, float]]:
    """Mock version of process_image_region for testing"""
    engine = MockOCREngine(lang=lang)

    # Load image if file path provided
    if isinstance(image, str):
        img_array = cv2.imread(image)
        if img_array is None:
            logger.error(f"Failed to load image from {image}")
            return {"text": "", "confidence": 0.0, "engine": "mock-tesseract"}
    else:
        img_array = image

    return engine.process_region(img_array, bbox)
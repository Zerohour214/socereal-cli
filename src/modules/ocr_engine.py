"""Wrapper around RapidOCR for performing recognition."""
import onnxruntime as ort
from rapidocr_onnxruntime import RapidOCR
from src.modules.preprocessing.roi import auto_crop_serial_region


class OCRService:
    """Lightweight wrapper around RapidOCR."""
    def __init__(self):
        """Initialize the OCR engine."""
        providers = ['CPUExecutionProvider']
        ort.set_default_logger_severity(3)
        self.ocr = RapidOCR(providers=providers)

    def __call__(self, image_path: str):
        """Run OCR on the provided image path and return raw results."""
        try:
            img = auto_crop_serial_region(image_path)
            result, _ = self.ocr(img)
            return result  # This is a list of (box, text, conf) tuples
        except Exception as e:
            from logging import error
            error(f"OCR error for {image_path}: {e}")
        return []

    def image_to_text(self, image_path: str) -> str:
        """Convenience wrapper returning plain text from OCR results."""
        result = self(image_path)
        if result:
            return " ".join([text for _, text, _ in result])
        return ""

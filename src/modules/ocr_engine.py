import onnxruntime as ort
from rapidocr_onnxruntime import RapidOCR
from src.modules.preprocessing.roi import auto_crop_serial_region


class OCRService:
    def __init__(self):
        providers = ['CPUExecutionProvider']
        ort.set_default_logger_severity(3)
        self.ocr = RapidOCR(providers=providers)

    def __call__(self, image_path: str):
        try:
            img = auto_crop_serial_region(image_path)
            result, _ = self.ocr(img)
            return result  # This is a list of (box, text, conf) tuples
        except Exception as e:
            from logging import error
            error(f"OCR error for {image_path}: {e}")
        return []

    def image_to_text(self, image_path: str) -> str:
        result = self(image_path)
        if result:
            return " ".join([text for _, text, _ in result])
        return ""

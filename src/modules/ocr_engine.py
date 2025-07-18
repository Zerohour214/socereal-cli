import onnxruntime as ort
from rapidocr_onnxruntime import RapidOCR

class OCRService:
    def __init__(self):
        providers = ['CPUExecutionProvider']
        ort.set_default_logger_severity(3)
        self.ocr = RapidOCR(providers=providers)

    def image_to_text(self, image_path: str) -> str:
        try:
            result, _ = self.ocr(image_path)
            if result:
                return " ".join([text for _, text, _ in result])
        except Exception as e:
            from logging import error
            error(f"OCR error for {image_path}: {e}")
        return ""

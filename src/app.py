from .modules.ocr_engine import OCRService
from .modules.file_utils import collect_image_files
from .adapters.csv_writer import write_ocr_results

def run_ocr_pipeline(inputs, output_csv):
    ocr_service = OCRService()
    files = collect_image_files(inputs)
    results = []
    for path in files:
        from logging import info
        info(f"OCR on: {path}")
        text = ocr_service.image_to_text(path)
        results.append((path, text))
    write_ocr_results(results, output_csv)
    from logging import info
    info(f"OCR results saved to: {output_csv}")

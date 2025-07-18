import logging
from .modules.ocr_engine import OCRService
from .modules.file_utils import collect_image_files
from .adapters.csv_writer import write_ocr_results
from .modules.validations.confidence_validation import validate_confidence, extract_text_and_conf
from .modules.validations.symbol_validation import validate_text
from .modules.validations.entropy_validation import text_entropy

def validate_entropy(text, min_e=2.0, max_e=5.5):
    e = text_entropy(text)
    if e < min_e or e > max_e:
        return f"Suspicious entropy: {e:.2f}"
    return "OK"

# Validation dispatch
VALIDATORS = {
    "confidence": lambda result, text: validate_confidence(result),
    "symbol": lambda result, text: validate_text(text),
    "entropy": lambda result, text: validate_entropy(text),
}

def run_ocr_pipeline(inputs, output_csv, validations=None):
    ocr_service = OCRService()
    files = collect_image_files(inputs)
    results = []

    if not validations:
        validations = ["confidence", "symbol", "entropy"]

    for path in files:
        logging.info(f"OCR on: {path}")
        # Always call the OCR service, get its output
        try:
            result = None
            if hasattr(ocr_service, "image_to_result"):
                result = ocr_service.image_to_result(path)
            elif hasattr(ocr_service, "__call__"):
                # Try to get all info from call (adapt for your service)
                result = ocr_service(path)
            else:
                result = ocr_service.image_to_text(path)
        except Exception as e:
            logging.error(f"OCR failed for {path}: {e}")
            result = ""
        text, conf_input = extract_text_and_conf(result)

        verdicts = []
        for v in validations:
            if v in VALIDATORS:
                if v == "confidence" and (conf_input is None or conf_input == []):
                    verdict = "confidence: Not supported"
                else:
                    verdict = VALIDATORS[v](conf_input, text)
                verdicts.append(f"{v}: {verdict}")
        results.append((path, text, "; ".join(verdicts)))


    write_ocr_results(results, output_csv)
    logging.info(f"OCR results saved to: {output_csv}")

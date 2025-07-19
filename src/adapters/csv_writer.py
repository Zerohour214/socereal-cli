"""Adapters for writing OCR results."""
import csv
import os

def write_ocr_results(results, output_csv):
    """Write OCR output records to a CSV file."""
    with open(output_csv, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "text", "validation"])
        for path, text, verdicts in results:
            writer.writerow([os.path.basename(path), text, verdicts])

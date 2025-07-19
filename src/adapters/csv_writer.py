"""Adapters for writing OCR results."""

import csv
from pathlib import Path

def write_ocr_results(results, output_csv):
    """Write OCR output records to a CSV file."""
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "text", "validation"])
        for path, text, verdicts in results:
            writer.writerow([Path(path).name, text, verdicts])

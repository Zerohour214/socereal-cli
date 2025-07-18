import csv
import os

def write_ocr_results(results, output_csv):
    with open(output_csv, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "text"])
        for path, text in results:
            writer.writerow([os.path.basename(path), text])

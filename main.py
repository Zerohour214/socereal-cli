import argparse
import os
import glob
import csv
import onnxruntime as ort
from rapidocr_onnxruntime import RapidOCR

class RapidOCR_CPU(RapidOCR):
    def __init__(self, *args, **kwargs):
        providers = ['CPUExecutionProvider']
        ort.set_default_logger_severity(3)
        super().__init__(*args, providers=providers, **kwargs)

def get_image_files(input_path):
    image_exts = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    files = []
    if os.path.isdir(input_path):
        for ext in image_exts:
            files.extend(glob.glob(os.path.join(input_path, ext)))
    elif '*' in input_path or '?' in input_path:
        for ext in image_exts:
            files.extend(glob.glob(input_path))
    elif os.path.isfile(input_path):
        files = [input_path]
    return sorted(set(files))

def run_ocr_on_files(files, output_csv):
    ocr = RapidOCR_CPU()
    with open(output_csv, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "text"])
        for img_path in files:
            print(f"[🔍] OCR on: {img_path}")
            result, _ = ocr(img_path)
            if result:
                text = " ".join([text for _, text, _ in result])
            else:
                text = ""
            writer.writerow([os.path.basename(img_path), text])
    print(f"[✅] Results saved to: {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Yeh Jpegs, and export to CSV")
    parser.add_argument("input", help="Image file, directory, or wildcard (e.g. ./images/*.jpg)")
    parser.add_argument("-o", "--output", default="ocr_results.csv", help="CSV output filename")
    args = parser.parse_args()

    files = get_image_files(args.input)
    if not files:
        print(f"[❌] No images found for: {args.input}")
    else:
        run_ocr_on_files(files, args.output)

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

def get_image_files(inputs):
    image_files = []
    for input_path in inputs:
        if os.path.isdir(input_path):
            # If it's a directory, add all image files inside
            for fname in os.listdir(input_path):
                fpath = os.path.join(input_path, fname)
                if os.path.isfile(fpath) and fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                    image_files.append(fpath)
        else:
            # If it's a file, just add it
            image_files.append(input_path)
    return image_files

def run_ocr_on_files(files, output_csv):
    ocr = RapidOCR_CPU()
    with open(output_csv, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "text"])
        for img_path in files:
            try:
                print(f"[🔍] OCR on: {img_path}")
                result, _ = ocr(img_path)
                if result:
                    text = " ".join([text for _, text, _ in result])
                else:
                    text = ""
                writer.writerow([os.path.basename(img_path), text])
            except Exception as e:
                print(f"[❌] Skipping {img_path}: {e}")
    print(f"[✅] Results saved to: {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Yeh Pegs, and export to CSV")
    parser.add_argument("input", nargs='+', help="Image file, directory, or wildcard (e.g. ./images/*.jpg)")
    parser.add_argument("-o", "--output", default="ocr_results.csv", help="CSV output filename")
    args = parser.parse_args()

    files = get_image_files(args.input)
    if not files:
        print(f"[❌] No images found for: {args.input}")
    else:
        run_ocr_on_files(files, args.output)

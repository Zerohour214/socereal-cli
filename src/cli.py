import argparse
from .modules.logging_utils import setup_logging
from .app import run_ocr_pipeline

def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI OCR tool: batch image-to-CSV"
    )
    parser.add_argument("input", nargs='+', help="Image file(s) or directory(s)")
    parser.add_argument("-o", "--output", default="ocr_results.csv", help="Output CSV filename")
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()
    run_ocr_pipeline(args.input, args.output)

if __name__ == "__main__":
    main()

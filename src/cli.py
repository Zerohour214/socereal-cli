"""Command-line interface for the OCR pipeline."""
import argparse
from pathlib import Path

from src.modules.logging_utils import setup_logging
from src.app import run_ocr_pipeline

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CLI OCR tool: batch image-to-CSV"
    )
    parser.add_argument("input", nargs='+', help="Image file(s) or directory(s)")
    parser.add_argument("-o", "--output", default="ocr_results.csv", help="Output CSV filename")
    parser.add_argument(
        "-v", "--validation",
        nargs='*',
        choices=["confidence", "symbol", "entropy"],
        help="Validation method(s) to run in sequence. If not set, defaults to: confidence symbol entropy."
    )
    return parser.parse_args()

def main():
    """Entry point used by console scripts."""
    setup_logging()
    args = parse_args()
    output = str(Path(args.output).expanduser())
    run_ocr_pipeline(args.input, output, args.validation)

if __name__ == "__main__":
    main()

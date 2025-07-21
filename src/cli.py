"""Command-line interface for the OCR pipeline."""
import argparse
from pathlib import Path
import textwrap
import glob

from src.modules.logging_utils import setup_logging
from src.app import run_ocr_pipeline


def parse_args():
    """Parse command line arguments."""
    example = textwrap.dedent(
        """Example usage:
        socereal images/*.png -o results.csv -v confidence symbol entropy

        This processes all PNG files, writes recognised text to results.csv.
        and runs the confidence, symbol and entropy validations in that order.
        """
    )
    parser = argparse.ArgumentParser(
        prog="socereal",
        description=(
            "SOCereal CLI: convert images to text in CSV format. "
            "Provide one or more image files or directories, and the OCR "
            "pipeline will process them into a CSV report."
        ),
        epilog=example,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                        help="Show this help message and exit")
    parser.add_argument(
        "input",
        nargs='+',
        help=(
            "Image file(s) or directory path(s) to process. Directories are "
            "scanned recursively for supported images."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="ocr_results.csv",
        metavar="FILE",
        help="CSV file to write OCR results to (default: %(default)s).",
    )
    parser.add_argument(
        "-v",
        "--validation",
        nargs='*',
        choices=["confidence", "symbol", "entropy"],
        metavar="STEP",
        help=(
            "Validation step(s) to run after OCR. 'confidence' checks the "
            "average OCR confidence, 'symbol' ensures only expected "
            "characters are present, and 'entropy' flags unusual text "
            "entropy. If omitted, all steps run in the order listed."
        ),
    )
    return parser.parse_args()

def main():
    """Entry point used by console scripts."""
    setup_logging()
    args = parse_args()
    output = str(Path(args.output).expanduser())

    # EXPAND INPUTS: wildcard/glob and directories
    expanded_inputs = []
    for arg in args.input:
        # Expand globs (wildcards) like images/*.jpg
        if '*' in arg or '?' in arg:
            files = glob.glob(arg)
            if not files:
                print(f"WARNING: No files matched: {arg}")
            expanded_inputs.extend(files)
        else:
            p = Path(arg)
            if p.is_dir():
                # Recursively gather image files from directories
                supported_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.webp')
                found = [str(f) for f in p.rglob("*") if f.suffix.lower() in supported_exts]
                if not found:
                    print(f"WARNING: No images found in directory: {arg}")
                expanded_inputs.extend(found)
            elif p.is_file():
                expanded_inputs.append(str(p))
            else:
                print(f"WARNING: Skipping unsupported input: {arg}")

    if not expanded_inputs:
        print("ERROR: No valid input files found. Nothing to do.")
        exit(1)

    # Pass to your pipeline
    run_ocr_pipeline(expanded_inputs, output, args.validation)

if __name__ == "__main__":
    main()

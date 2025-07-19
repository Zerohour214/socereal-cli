# Socereal CLI

**Socereal CLI** is a small command line utility that performs Optical Character Recognition (OCR) on a batch of image files and writes the collected text to a CSV file. It leverages [RapidOCR](https://github.com/RapidAI/RapidOCR) via ONNX Runtime and includes several validation helpers to spot potential issues in the OCR output.

## Features

- Batch process individual images or entire directories
- Automatically crops the region of interest before OCR
- Validation options:
  - **confidence** – checks the average confidence score from the OCR engine
  - **symbol** – warns about unusual characters
  - **entropy** – flags text that is statistically different from the rest
- Outputs results as `filename,text,validation` in a CSV file

## Project Structure

```
src/
  adapters/         # I/O adapters (e.g. CSV writer)
  modules/          # OCR engine and various helper utilities
  app.py            # Core OCR pipeline
  cli.py            # Command line interface entry point
images/             # Example images for testing the CLI
tests/              # Unit tests
```

## Requirements

- Python 3.8 or higher
- [`rapidocr-onnxruntime`](https://pypi.org/project/rapidocr-onnxruntime/)
- [`onnxruntime`](https://pypi.org/project/onnxruntime/)

For development and running the tests you will also need:

- `numpy`
- `opencv-python`
- `pytest`

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd socereal-cli
   ```
2. **Create and activate a virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the runtime dependencies**
   ```bash
   pip install -r requirements.txt
   pip install opencv-python numpy  # needed for preprocessing and validations
   ```
4. **(Optional) Install test/development tools**
   ```bash
   pip install pytest
   ```

## Usage

The CLI is invoked via the `src.cli` module. Supply one or more image files or directories as input. By default all validations are run.

```bash
python -m src.cli input_folder -o results.csv
```

You can limit or reorder the validation steps with `-v/--validation`:

```bash
python -m src.cli image1.jpg image2.png \
    -v confidence symbol -o output.csv
```

The CSV will contain three columns: `filename`, `text`, and the combined validation result for each file.

## Development

To run the test suite:

```bash
pytest
```

The tests cover validation helpers and a minimal OCR pipeline harness. They are a good starting point when adding new features.

Logging is configured to output simple informational messages. Feel free to adjust the logging settings in `src/modules/logging_utils.py`.

## Contributing

Pull requests are welcome! If you plan on contributing major changes, please open an issue first to discuss what you would like to change.

---

**Socereal CLI** is provided as-is with no warranty. It is intended as a lightweight starting point for more advanced OCR workflows.

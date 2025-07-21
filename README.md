# SoCereal CLI

SoCereal is a command-line tool for running Optical Character Recognition (OCR) on
batches of images. It wraps the [RapidOCR](https://github.com/RapidAI/RapidOCR)
engine and produces a CSV report containing the recognized text along with several
validation checks.

This document serves as the main documentation for the project. Each section can
be navigated like a wiki using the table of contents below.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Validations](#validations)
- [Application Structure](#application-structure)
- [Running the Tests](#running-the-tests)
- [Deploying as a Standalone Binary](#deploying-as-a-standalone-binary)

## Overview
The CLI accepts one or more image files or directories and outputs the OCR
results to a CSV file. A typical invocation looks like:

```bash
socereal.exe image\* -o result.csv
```

By default it performs OCR on every image, runs a few validation routines, and
writes the results to the specified CSV.

## Features
- Batch OCR using RapidOCR with ONNX Runtime
- Optional pre-processing that automatically crops the central region of each
  image for better accuracy
- CSV output including the filename, recognized text and validation verdicts
- Built-in validation methods:
  - **confidence** – checks the average confidence of the OCR engine
  - **symbol** – flags abnormal characters in the text
  - **entropy** – warns if the text entropy is suspiciously high or low
- Runs on Python 3.11.9 or newer and can be packaged as a standalone executable

## Installation
1. Ensure you have **Python 3.11.9** available on your system and add to PATH.
2. Install dependencies and the package itself:

```bash
pip install -r requirements.txt
pip install .
```

On Windows you can simply run `install.bat`, which creates a virtual
environment, installs everything and builds a single `socereal.exe` binary. On
Linux/macOS the `install.sh` script performs a similar setup and attempts to
place the `socereal` command on your `PATH`.

## Quickstart
After installation the basic usage is:

```bash
socereal <images or folders> -o output.csv
```

For example:

```bash
socereal ./images -o ocr_results.csv
```

The script will scan the given paths for supported image files (`.png`, `.jpg`,
`.jpeg`, `.bmp`, `.tiff`, `.gif`), run OCR and validations, then create the CSV
report.

## Usage
The CLI supports a few options which can be inspected with `--help`:

```bash
socereal --help
```

Important parameters:

- `input` – one or more image paths or directories
- `-o, --output` – name of the output CSV file (default: `ocr_results.csv`)
- `-v, --validation` – specify which validations to run; if omitted all three are
  executed (confidence, symbol and entropy)

## Validations
Each OCR result can be checked by one or more validation routines:

- **Confidence** – warns if the average OCR confidence is below a threshold.
- **Symbol** – reports if abnormal characters are present (e.g. emoji or
  non-ASCII symbols).
- **Entropy** – computes Shannon entropy of the text to detect anomalies.

You may choose which validations to run by listing them after `-v`:

```bash
socereal img.png -v confidence symbol -o out.csv
```

## Application Structure
```
src/
├── cli.py             # Entry point for the command line interface
├── app.py             # Orchestrates the OCR pipeline
├── adapters/
│   └── csv_writer.py  # Writes CSV reports
├── modules/
│   ├── ocr_engine.py  # Wrapper around RapidOCR
│   ├── preprocessing/ # Image pre-processing utilities
│   ├── validations/   # Validation helpers
│   └── file_utils.py  # Collects image paths
```
Other notable directories:

- `tests/` – unit tests for the main modules
- `images/` – sample images or placeholders used during development
- `install.bat` / `install.sh` – scripts to set up and package the tool

## Running the Tests
Tests are written with `pytest`. Install the additional dependencies and run:

```bash
pip install pytest pyfakefs
pytest
```

They exercise the validation logic and file utilities on various platforms.

## Deploying as a Standalone Binary
The Windows installer (`install.bat`) builds a single executable using
PyInstaller. After running the script you will find `socereal.exe` in the project
root. The Linux installer attempts the same if it cannot place the script on your
`PATH`. This allows distribution of the tool without requiring a Python
interpreter on the target machine.

---
SoCereal is released under the MIT License and welcomes contributions via pull
requests.

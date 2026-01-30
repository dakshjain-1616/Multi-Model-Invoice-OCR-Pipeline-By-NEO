# Invoice NER Pipeline

This project automates the extraction of entities from invoice images using a BERT-based Named Entity Recognition (NER) model and Tesseract OCR.

## Prerequisites

- **Python 3.8+**
- **Tesseract OCR**: Required for image-to-text conversion.
  - macOS: `brew install tesseract`
  - Ubuntu: `sudo apt-get install tesseract-ocr`

## Getting Started

To set up the environment, install dependencies, and run the pipeline in one go, use the provided automation scripts:

### macOS / Linux
```bash
./run_project.sh
```

### Windows (or Manual Python)
```bash
python run_project.py
```

## Project Structure

- `invoice_pipeline.py`: Main entry point for the prediction pipeline.
- `model/`: Directory containing the trained BERT model and tokenizer.
- `data/`: Sample data and labels.
- `config.py`: Global configuration and paths.
- `check_environment.py`: Helper to verify system dependencies.

## Output

The pipeline produces:
1. `output_results.json`: Extracted entities (Vendor, Invoice Date, Total, etc.).
2. Logs printed to terminal regarding OCR and model inference status.
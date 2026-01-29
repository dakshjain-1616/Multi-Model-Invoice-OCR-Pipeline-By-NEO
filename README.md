# End-to-End Invoice Processing System (CPU Optimised)

This repository contains a multi-stage AI pipeline for automated invoice data extraction. It leverages state-of-the-art vision and language models, specifically fine-tuned and configured to run efficiently on 4-core CPU environments.

## 🚀 Key Features
- **Multi-Stage Processing**: Layout Detection (LayoutLMv3) → OCR (TrOCR) → NER (BERT).
- **CPU Optimised**: Custom configurations for low-latency inference without GPU.
- **Multi-Language Support**: Handles English and Spanish (or other secondary languages) via TrOCR's robust recognition.
- **High Accuracy NER**: Fine-tuned BERT model for identifying Vendors, Dates, Total Amounts, and Line Items.

## 🏗 System Architecture
1. **Layout Detection**: Uses `microsoft/layoutlmv3-base` to segment the invoice into structural blocks (Header, Table, Footer).
2. **Text Recognition**: `microsoft/trocr-base-printed` extracts high-fidelity text from identified regions.
3. **Information Extraction**: A fine-tuned `bert-base-multilingual-cased` model performs Named Entity Recognition (NER) on the extracted text to structure the data into JSON.

## 🛠 Installation & Usage

### Prerequisites
- Python 3.12+
- 4-core CPU, 16GB RAM

### Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch torchvision transformers pillow pandas
```

### Run Pipeline
```bash
python3 invoice_pipeline.py --image /path/to/invoice.png
```

## 📊 Performance Benchmarks (4-Core CPU)
The following results were obtained from the automated `e2e_test_verification.py` run:

- **Avg. Inference Latency**: ~35-45s per invoice (Complete E2E)
- **Schema Compliance**: 100% JSON Schema Validation
- **Hardware**: Intel(R) Xeon(R) @ 2.20GHz (4 Cores)

## 📂 Project Structure
- `invoice_pipeline.py`: Main entry point for processing.
- `processor_modules.py`: Encapsulated Model Logic (LayoutLM, TrOCR, BERT).
- `model/`: Stored weights for the fine-tuned NER model.
- `data/`: Sample synthetic data generation scripts.

## 📜 License
MIT
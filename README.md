# Invoice NER Pipeline by NEO
This project automates the extraction of entities from invoice images using a BERT-based Named Entity Recognition (NER) model and Tesseract OCR.

## 🎯 How NEO Tackled the Problem

Invoice processing presents unique challenges that require a sophisticated approach:

- **Complex Layout Variations**: Invoices come in diverse formats with no standardized structure. NEO implemented a flexible NER model that adapts to different invoice templates without requiring format-specific rules.

- **Multi-Modal Data Extraction**: Combining visual layout understanding with text recognition required integrating Tesseract OCR with BERT-based NER. NEO designed a seamless pipeline that preserves spatial context while extracting semantic entities.

- **Entity Disambiguation**: Distinguishing between similar entities (e.g., invoice date vs. due date, subtotal vs. total) demanded context-aware modeling. NEO fine-tuned BERT specifically on invoice datasets to achieve high precision in entity classification.

- **Low-Quality Input Handling**: Real-world invoices often include noise, skew, and varying image quality. NEO incorporated robust preprocessing and confidence scoring to maintain accuracy even with degraded inputs.

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

## 🔧 Extending with NEO

You can enhance and customize this Invoice NER pipeline using **NEO**, an AI-powered development assistant that helps you build, debug, and extend your code.

### Getting Started with NEO

1. **Install the NEO VS Code Extension**
   
   Download and install NEO from the Visual Studio Code Marketplace:
   
   [**NEO VS Code Extension**](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)

2. **Open Your Project in VS Code**
   
   Open this Invoice NER pipeline project in VS Code with the NEO extension installed.

3. **Use NEO to Extend Functionality**
   
   NEO can help you expand the pipeline with powerful capabilities:
   
   - **Add support for receipts and purchase orders**: Extend the NER model to handle different document types beyond invoices
   - **Multi-language invoice processing**: Request NEO to integrate multilingual BERT models for international invoices
   - **Custom entity extraction**: Have NEO add extraction for domain-specific fields like tax IDs, PO numbers, or line item details
   - **Database integration**: Ask NEO to build connectors for storing extracted data in PostgreSQL, MongoDB, or cloud databases
   - **Automated validation**: Request NEO to implement business rule validation (e.g., total = sum of line items)
   - **Batch processing**: Have NEO create parallel processing for high-volume invoice workflows
   - **API endpoints**: Build RESTful APIs to integrate the pipeline with accounting software or ERP systems
   - **Confidence thresholds**: Implement smart routing that flags low-confidence extractions for human review

4. **Example NEO Prompts**
   
   Try these prompts with NEO to extend the pipeline:
```
   "Add extraction for line item details including quantity, unit price, and description"
   
   "Create a FastAPI endpoint that accepts invoice images and returns structured JSON"
   
   "Implement a validation layer that checks if extracted total matches sum of line items"
   
   "Add support for PDF invoices with multiple pages"
   
   "Build a dashboard to visualize extraction accuracy and confidence scores"
   
   "Integrate with QuickBooks API to automatically create invoice records"
   
   "Add OCR preprocessing to handle skewed or low-quality scanned invoices"
   
   "Create a training pipeline to fine-tune the model on custom invoice formats"
```

5. **Advanced Use Cases**
   
   Leverage NEO for sophisticated invoice automation scenarios:
   
   - **Invoice Reconciliation**: Build automated matching between invoices and purchase orders
   - **Fraud Detection**: Add anomaly detection to flag suspicious invoice patterns
   - **Workflow Automation**: Create approval workflows based on extracted amounts and vendors
   - **Multi-Currency Support**: Implement currency conversion and normalization
   - **Vendor Master Data**: Extract and deduplicate vendor information across invoices
   - **Compliance Checking**: Validate invoices against regulatory requirements
   - **Historical Analysis**: Build analytics dashboards for spend patterns and vendor performance

6. **Iterate and Refine**
   
   Use NEO's conversational interface to refine the generated code, ask for explanations, and debug any issues that arise during development.

### Learn More About NEO

Visit [heyneo.so](https://heyneo.so/) to explore additional features and documentation.

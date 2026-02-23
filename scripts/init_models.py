import os
import torch
import sys
from pathlib import Path
from transformers import (
    LayoutLMv3Processor,
    AutoTokenizer, AutoModelForTokenClassification
)

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def download_models():
    print(f"Python path: {sys.executable}")
    
    print("Downloading LayoutLMv3 Processor...")
    LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
    
    print("Downloading BERT NER model for invoice extraction...")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForTokenClassification.from_pretrained(
        "bert-base-uncased", 
        num_labels=5  # O, VENDOR, DATE, ITEM, TOTAL
    )
    
    # Save to local directory
    ner_model_path = PROJECT_ROOT / "models" / "invoice_ner_bert"
    ner_model_path.mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(ner_model_path)
    model.save_pretrained(ner_model_path)
    print(f"Saved NER model to {ner_model_path}")
    
    print("\nEnvironment check:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    print("\nNote: This project now uses OpenRouter for OCR.")
    print("Set your OPENROUTER_API_KEY in .env file before running the pipeline.")

if __name__ == "__main__":
    try:
        download_models()
        print("\nModel initialization successful.")
    except Exception as e:
        print(f"Error during model initialization: {e}")
        sys.exit(1)
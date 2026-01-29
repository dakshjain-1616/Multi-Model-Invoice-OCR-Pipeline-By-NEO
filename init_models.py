import os
import torch
import sys
from transformers import (
    LayoutLMv3Processor,
    TrOCRProcessor, VisionEncoderDecoderModel,
    AutoTokenizer, AutoModelForTokenClassification
)

def download_models():
    print(f"Python path: {sys.executable}")
    
    print("Downloading LayoutLMv3 Processor...")
    # Using processor only for now as weights are large and we will fine-tune or load specific checkpoints
    LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
    
    print("Downloading TrOCR...")
    TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    
    print("Downloading Multilingual BERT...")
    AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
    AutoModelForTokenClassification.from_pretrained("bert-base-multilingual-cased")
    
    print("Environment check:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")

if __name__ == "__main__":
    try:
        download_models()
        print("Model initialization successful.")
    except Exception as e:
        print(f"Error during model initialization: {e}")
        sys.exit(1)
import torch
from transformers import AutoProcessor
import sys
import os

# Base path
PROJECT_ROOT = "/Users/dakshjain/Desktop/OCR-update/Multi-Model-Invoice-OCR-Pipeline"
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "glm-ocr")

def verify_structure():
    print(f"Verifying GLM-OCR structure at {MODEL_PATH}...")
    
    if not os.path.exists(MODEL_PATH):
        print("FAIL: Model directory missing.")
        return False
        
    try:
        # We only try to load the processor - it's much lighter than the 2.5GB model
        # and verifies trust_remote_code and custom class mapping.
        print("Instantiating AutoProcessor (structural test)...")
        processor = AutoProcessor.from_pretrained(MODEL_PATH, trust_remote_code=True)
        print(f"SUCCESS: Processor instantiated. Class: {type(processor)}")
        
        # Check if model file exists
        weights_path = os.path.join(MODEL_PATH, "model.safetensors")
        if os.path.exists(weights_path):
            size_gb = os.path.getsize(weights_path) / (1024**3)
            print(f"SUCCESS: Weights found ({size_gb:.2f} GB)")
        else:
            print("FAIL: Weights missing (model.safetensors)")
            return False
            
        return True
    except Exception as e:
        print(f"FAIL: Error during structural verification: {e}")
        return False

if __name__ == "__main__":
    success = verify_structure()
    sys.exit(0 if success else 1)

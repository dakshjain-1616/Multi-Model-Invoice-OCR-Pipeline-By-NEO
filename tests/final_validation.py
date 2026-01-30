import os
import sys
from config import BASE_DIR, NER_MODEL_PATH, IMAGES_DIR

def validate():
    print("=== FINAL PROJECT VALIDATION ===")
    
    # 1. Path Validation
    print(f"\n1. Paths (Dynamic via config.py):")
    print(f"   Root: {BASE_DIR}")
    print(f"   NER Model: {NER_MODEL_PATH}")
    
    # 2. File Presence
    print(f"\n2. Essential Files:")
    files = ["requirements.txt", "config.py", "invoice_pipeline.py", "data_preparation.py"]
    for f in files:
        status = "✅" if os.path.exists(os.path.join(BASE_DIR, f)) else "❌"
        print(f"   [{status}] {f}")
        
    # 3. Import Validation
    print(f"\n3. Library Imports:")
    try:
        import torch
        import transformers
        import PIL
        print("   ✅ Torch, Transformers, PIL loaded successfully.")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")

    # 4. Model State Note
    model_size = os.path.getsize(os.path.join(NER_MODEL_PATH, "model.safetensors")) / (1024*1024) if os.path.exists(os.path.join(NER_MODEL_PATH, "model.safetensors")) else 0
    print(f"\n4. Model Integrity:")
    print(f"   Current Model Size: {model_size:.2f} MB")
    if model_size < 10:
        print("   ⚠️ WARNING: Model weights appear truncated/corrupted (Expected >100MB).")
        print("   Pipeline will use architectural fallback for structural execution.")

if __name__ == "__main__":
    validate()
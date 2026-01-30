import os
from pathlib import Path

# Base directory: /Users/dakshjain/Desktop/GitHubDemos/NEODEMO1
# Since config.py is in src/, PROJECT_ROOT is the parent directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
DATASET_PATH = DATA_DIR / "dataset.json"

# Model paths
MODEL_DIR = PROJECT_ROOT / "models"
NER_MODEL_PATH = MODEL_DIR / "invoice_ner_bert"

# Output paths
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_RESULTS = PROJECT_ROOT / "output_results.json"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
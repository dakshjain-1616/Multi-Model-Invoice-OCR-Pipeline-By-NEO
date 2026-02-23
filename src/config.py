import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory: /Users/dakshjain/Desktop/GitHubDemos/NEODEMO1
# Since config.py is in src/, PROJECT_ROOT is the parent directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
DATASET_PATH = DATA_DIR / "dataset.json"

# Model paths
MODEL_DIR = PROJECT_ROOT / "models"
NER_MODEL_PATH = MODEL_DIR / "invoice_ner_bert"
OCR_MODEL_ID = "zai-org/GLM-OCR"

# OpenRouter Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
# GLM-4.5V vision model on OpenRouter (supports image input for OCR tasks)
# This is the closest equivalent to GLM-OCR on OpenRouter
OPENROUTER_MODEL = "z-ai/glm-4.5v"  # GLM vision model for OCR

# Output paths
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_RESULTS = PROJECT_ROOT / "output_results.json"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
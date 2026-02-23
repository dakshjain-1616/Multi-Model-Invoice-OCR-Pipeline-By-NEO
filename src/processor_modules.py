import torch
from PIL import Image
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification, TrOCRProcessor, VisionEncoderDecoderModel
import pytesseract

class InvoiceLayoutDetector:
    def __init__(self):
        self.processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
        # We use a base model; in a real scenario, this would be fine-tuned for DLA.
        # For this pipeline, we leverage its capability to process image + text + boxes.
        self.model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base", num_labels=5)
        self.model.eval()

    def detect_regions(self, image):
        # LayoutLMv3 typically needs words and boxes from OCR (pytesseract)
        encoding = self.processor(image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**encoding)
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification, AutoProcessor

class InvoiceOCRGLM:
    def __init__(self):
        try:
            from .config import OCR_MODEL_ID, PROJECT_ROOT
        except (ImportError, ValueError):
            from config import OCR_MODEL_ID, PROJECT_ROOT
        
        # Priority: Local path if files exist, then HuggingFace ID
        local_path = PROJECT_ROOT / "models" / "glm-ocr"
        if (local_path / "config.json").exists():
            self.model_id = str(local_path)
            print(f"Using local GLM-OCR model path: {self.model_id}")
        else:
            self.model_id = OCR_MODEL_ID
            print(f"Loading GLM-OCR model from HF: {self.model_id}")
        
        self.processor = AutoProcessor.from_pretrained(self.model_id, trust_remote_code=True)
        # Load in float16/bfloat16 for efficiency
        self.model = AutoModelClass.from_pretrained(
            self.model_id, 
            trust_remote_code=True,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True,
            device_map="auto" if torch.cuda.is_available() else None
        )
        self.model.eval()

    def recognize_text(self, image, box=None):
        # Crop the image to the bounding box if provided
        if box:
            left, top, right, bottom = box
            img_to_proc = image.crop((left, top, right, bottom))
        else:
            img_to_proc = image

        prompt = "Transcribe this document."
        messages = [
            {"role": "user", "content": prompt},
            {"role": "image", "content": img_to_proc},
        ]
        
        # Prepare inputs
        inputs = self.processor.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
        
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=512)
        
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text

class InvoiceOCRTrOCR:
    # Kept for backward compatibility if needed, but replaced by GLM in pipeline
    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        self.model.eval()

    def recognize_text(self, image, box):
        # Crop the image to the bounding box
        left, top, right, bottom = box
        crop = image.crop((left, top, right, bottom))
        pixel_values = self.processor(images=crop, return_tensors="pt").pixel_values
        
        with torch.no_grad():
            generated_ids = self.model.generate(pixel_values)
        
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text

if __name__ == "__main__":
    # Smoke test
    print("Initializing modules...")
    layout_detector = InvoiceLayoutDetector()
    ocr_engine = InvoiceOCRGLM()
    
    # Load a synthetic image
    test_img = Image.open("data/images/invoice_0.png").convert("RGB")
    
    print("Testing Layout Detection (encoding)...")
    enc, out = layout_detector.detect_regions(test_img)
    print(f"Layout encoding words shape: {enc['input_ids'].shape}")
    
    print("Testing GLM-OCR on a sample region...")
    # Using a known region from our synthetic data for validation
    sample_box = [50, 50, 400, 100] # Approximate vendor area
    text = ocr_engine.recognize_text(test_img, sample_box)
    print(f"OCR Result: {text}")
    print("Modules verification complete.")
import torch
import base64
import io
from PIL import Image
from transformers import (
    LayoutLMv3Processor, 
    LayoutLMv3ForTokenClassification, 
    TrOCRProcessor, 
    VisionEncoderDecoderModel,
    AutoProcessor,
    AutoModelForImageTextToText
)
import pytesseract
from openai import OpenAI

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


class InvoiceOCRGLM:
    """GLM-OCR based OCR engine for invoice text recognition."""
    
    def __init__(self):
        try:
            from .config import OCR_MODEL_ID, PROJECT_ROOT
        except (ImportError, ValueError):
            from config import OCR_MODEL_ID, PROJECT_ROOT
        
        # Priority: Local path if files exist, then HuggingFace ID
        local_path = PROJECT_ROOT / "models" / "glm-ocr"
        if (local_path / "config.json").exists() and (local_path / "model.safetensors").exists():
            self.model_id = str(local_path)
            print(f"Using local GLM-OCR model path: {self.model_id}")
        else:
            self.model_id = OCR_MODEL_ID
            print(f"Loading GLM-OCR model from HF: {self.model_id}")
        
        self.processor = AutoProcessor.from_pretrained(self.model_id, trust_remote_code=True)
        # Load model using AutoModelForImageTextToText as per GLM-OCR documentation
        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_id, 
            trust_remote_code=True,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
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

        # Use the correct message format as per GLM-OCR documentation
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": img_to_proc,
                    },
                    {
                        "type": "text",
                        "text": "Text Recognition:"
                    }
                ],
            }
        ]
        
        # Prepare inputs using apply_chat_template
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )
        
        # Remove token_type_ids if present (as per GLM-OCR docs)
        inputs.pop("token_type_ids", None)
        
        # Move inputs to model device
        inputs = {k: v.to(self.model.device) if hasattr(v, 'to') else v for k, v in inputs.items()}
        
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=8192)
        
        # Decode only the generated part (skip input tokens)
        input_len = inputs["input_ids"].shape[1]
        generated_text = self.processor.decode(generated_ids[0][input_len:], skip_special_tokens=True)
        return generated_text


class InvoiceOCROpenRouter:
    """OpenRouter-based OCR engine using GLM-4.5V vision model for invoice text recognition.
    
    Note: The original Hugging Face model 'zai-org/GLM-OCR' is a specialized OCR model.
    On OpenRouter, 'z-ai/glm-4.5v' is the closest equivalent - a GLM vision model that
    supports image input and can perform OCR tasks.
    """
    
    def __init__(self):
        try:
            from .config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
        except (ImportError, ValueError):
            from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL
        
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please set the OPENROUTER_API_KEY environment variable."
            )
        
        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
        )
        self.model = OPENROUTER_MODEL
        print(f"Initialized OpenRouter OCR with model: {self.model}")
    
    def _image_to_base64(self, image):
        """Convert PIL Image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")
    
    def recognize_text(self, image, box=None):
        """Recognize text from image using OpenRouter's GLM-4V model."""
        # Crop the image to the bounding box if provided
        if box:
            left, top, right, bottom = box
            img_to_proc = image.crop((left, top, right, bottom))
        else:
            img_to_proc = image
        
        # Convert image to base64
        base64_image = self._image_to_base64(img_to_proc)
        
        # Create the message with image
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract all text from this invoice image. Return only the text content without any additional commentary."
                        }
                    ]
                }
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content


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
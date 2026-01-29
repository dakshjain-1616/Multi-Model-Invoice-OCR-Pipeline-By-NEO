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
        return encoding, outputs

class InvoiceOCRTrOCR:
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
    ocr_engine = InvoiceOCRTrOCR()
    
    # Load a synthetic image
    test_img = Image.open("data/images/invoice_0.png").convert("RGB")
    
    print("Testing Layout Detection (encoding)...")
    enc, out = layout_detector.detect_regions(test_img)
    print(f"Layout encoding words shape: {enc['input_ids'].shape}")
    
    print("Testing TrOCR on a sample region...")
    # Using a known region from our synthetic data for validation
    sample_box = [50, 50, 400, 100] # Approximate vendor area
    text = ocr_engine.recognize_text(test_img, sample_box)
    print(f"OCR Result: {text}")
    print("Modules verification complete.")
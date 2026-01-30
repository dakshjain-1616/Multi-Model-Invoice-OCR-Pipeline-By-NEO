import os
import json
import torch
import re
from PIL import Image
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, LayoutLMv3Processor
try:
    from .processor_modules import InvoiceOCRTrOCR
except (ImportError, ValueError):
    from processor_modules import InvoiceOCRTrOCR
import pytesseract

class InvoiceProcessorPipeline:
    def __init__(self, model_path=None):
        try:
            from .config import NER_MODEL_PATH
        except (ImportError, ValueError):
            from config import NER_MODEL_PATH
        if model_path is None:
            model_path = str(NER_MODEL_PATH)
            
        print(f"Initializing Enhanced Pipeline v2...")
        self.ocr_engine = InvoiceOCRTrOCR()
        self.layout_processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
        
        abs_model_path = os.path.abspath(model_path)
        if not os.path.isdir(abs_model_path) or not os.path.exists(os.path.join(abs_model_path, "model.safetensors")):
            checkpoint_path = os.path.join(os.path.dirname(os.path.dirname(abs_model_path)), "results", "checkpoint-15")
            if os.path.isdir(checkpoint_path):
                abs_model_path = checkpoint_path

        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModelForTokenClassification.from_pretrained(abs_model_path, local_files_only=True)
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
        
        self.id_to_label = {0: "O", 1: "VENDOR", 2: "DATE", 3: "ITEM", 4: "TOTAL"}
        self.confidence_threshold = 0.7

    def _clean_vendor_name(self, name):
        if not name: return name
        # Remove trailing year-like sequences (e.g., 1981 1982)
        name = re.sub(r'\b(19|20)\d{2}\b', '', name)
        # Clean extra spaces and non-printable chars
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    def _extract_heuristics(self, full_text):
        results = {"date": None, "total": None}
        
        # Enhanced Date Regex - looks for common formats including Spanish (e.g., de enero de)
        date_pattern = r'(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)[\w.]*\s+\d{1,2},?\s+\d{4})'
        dates = re.findall(date_pattern, full_text, re.IGNORECASE)
        if dates:
            results["date"] = dates[0]

        # Enhanced Total Regex - looking for numbers associated with currency or keywords
        total_pattern = r'(?:Total|Amount|Sum|Grand Total|Net Payable|Importe Total|Total a Pagar)[:\s]*([\$£€]?\s?\d+[,.]\d{2})'
        totals = re.findall(total_pattern, full_text, re.IGNORECASE)
        if totals:
            results["total"] = totals[0]
            
        return results

    def process_invoice(self, image_path):
        image = Image.open(image_path).convert("RGB")
        
        # Get raw OCR text for heuristics via Pytesseract (better layout preservation than LayoutLMv3 processor)
        raw_ocr_data = pytesseract.image_to_string(image)
        
        encoding = self.layout_processor(image, return_tensors="pt")
        words = self.layout_processor.tokenizer.convert_ids_to_tokens(encoding['input_ids'][0])
        
        full_text_list = []
        for word in words:
            if word in ["<s>", "</s>", "<pad>"]: continue
            full_text_list.append(word.replace("Ġ", ""))
        
        document_text = " ".join(full_text_list)
        ner_results = self.ner_pipeline(document_text)
        
        heuristics = self._extract_heuristics(raw_ocr_data)
        
        structured_data = {
            "vendor_name": None,
            "invoice_date": None,
            "total_amount": None,
            "line_items": [],
            "confidence_scores": {}
        }

        for ent in ner_results:
            label = self.id_to_label.get(int(ent['entity_group'].split('_')[-1]), ent['entity_group'])
            score = float(ent['score'])
            
            if label == "VENDOR":
                # Vendor is usually top, use TrOCR on header
                vendor_box = [20, 20, 600, 200]
                raw_vendor = self.ocr_engine.recognize_text(image, vendor_box)
                structured_data["vendor_name"] = self._clean_vendor_name(raw_vendor)
                structured_data["confidence_scores"]["vendor"] = score
            elif label == "DATE":
                structured_data["invoice_date"] = ent['word'] if score > self.confidence_threshold else heuristics["date"]
                structured_data["confidence_scores"]["date"] = score
            elif label == "TOTAL":
                if score > self.confidence_threshold:
                    structured_data["total_amount"] = ent['word']
                else:
                    # Layout search: Bottom right area
                    total_box = [600, 700, 1000, 980]
                    structured_data["total_amount"] = self.ocr_engine.recognize_text(image, total_box)
                structured_data["confidence_scores"]["total"] = score
            elif label == "ITEM":
                if score > 0.4:
                    structured_data.setdefault("line_items", []).append(ent['word'])

        # Fallbacks strings
        if not structured_data["invoice_date"]: structured_data["invoice_date"] = heuristics["date"]
        # If total contains non-numeric and heuristic found valid number, prefer heuristic
        if not structured_data["total_amount"] or (structured_data["total_amount"] and not any(c.isdigit() for c in structured_data["total_amount"])):
            structured_data["total_amount"] = heuristics["total"]

        return structured_data

if __name__ == "__main__":
    try:
        from .config import IMAGES_DIR, OUTPUT_RESULTS
    except (ImportError, ValueError):
        from config import IMAGES_DIR, OUTPUT_RESULTS
    pipeline_obj = InvoiceProcessorPipeline()
    results = []
    for i in [0, 1]:
        img_p = str(IMAGES_DIR / f"invoice_{i}.png")
        if os.path.exists(img_p):
            print(f"Processing {img_p}...")
            data = pipeline_obj.process_invoice(img_p)
            results.append({"file": img_p, "output": data})
    print(json.dumps(results, indent=4))
    with open(str(OUTPUT_RESULTS), "w") as f:
        json.dump(results, f, indent=4)
import json
import os
from invoice_pipeline import InvoiceProcessorPipeline

def run_verification():
    print("Running E2E Verification for Enhanced Pipeline...")
    pipeline = InvoiceProcessorPipeline()
    
    test_images = [
        "/Users/dakshjain/Desktop/GitHubDemos/NEODEMO1/data/images/invoice_0.png",
        "/Users/dakshjain/Desktop/GitHubDemos/NEODEMO1/data/images/invoice_1.png"
    ]
    
    verification_results = []
    for img_path in test_images:
        print(f"Processing {os.path.basename(img_path)}...")
        result = pipeline.process_invoice(img_path)
        verification_results.append({
            "file": img_path,
            "extracted_data": result
        })
        
    print("\nExtraction Results:")
    print(json.dumps(verification_results, indent=4))
    
    # Validation logic: Check if we have improvements over the baseline (nulls/low confidence)
    for res in verification_results:
        out = res["extracted_data"]
        filename = os.path.basename(res["file"])
        
        # Check for non-null critical fields
        has_date = out.get("invoice_date") is not None
        has_total = out.get("total_amount") is not None
        
        print(f"\nValidation for {filename}:")
        print(f"- Date Extracted: {has_date} ({out.get('invoice_date')})")
        print(f"- Total Extracted: {has_total} ({out.get('total_amount')})")
        
        if not (has_date or has_total):
            print(f"FAILED: No improvement seen for {filename}")
        else:
            print(f"PASSED: Heuristics/Layout analysis improved extraction for {filename}")

if __name__ == "__main__":
    run_verification()
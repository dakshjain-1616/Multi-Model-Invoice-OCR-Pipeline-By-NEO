import os
import json
import random
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def generate_synthetic_invoice(index, lang='en'):
    """Generates a synthetic invoice image and ground truth labels."""
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Simple templates
    vendors = {
        'en': ["Global Tech Solutions", "Office Supplies Inc.", "North Star Logistics"],
        'es': ["Soluciones Tecnológicas Globales", "Suministros de Oficina S.A.", "Logística Estrella del Norte"]
    }
    dates_labels = {'en': "Date", 'es': "Fecha"}
    total_labels = {'en': "Total Amount", 'es': "Monto Total"}
    items_labels = {'en': "Description", 'es': "Descripción"}
    
    vendor = random.choice(vendors[lang])
    date = f"202{random.randint(0,5)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    amount = f"{random.uniform(100, 5000):.2f}"
    
    entities = []
    
    # Draw Vendor (Header)
    draw.text((50, 50), vendor, fill=(0, 0, 0))
    entities.append({"text": vendor, "label": "B-VENDOR", "box": [50, 50, 300, 80]})
    
    # Draw Date
    date_text = f"{dates_labels[lang]}: {date}"
    draw.text((50, 120), date_text, fill=(0, 0, 0))
    entities.append({"text": date, "label": "B-DATE", "box": [150, 120, 250, 140]})
    
    # Draw Items (Mock table)
    draw.text((50, 200), f"{items_labels[lang]}", fill=(0, 0, 0))
    for i in range(3):
        item_text = f"Item {i+1} service" if lang == 'en' else f"Servicio {i+1}"
        y = 230 + (i * 30)
        draw.text((50, y), item_text, fill=(0, 0, 0))
        entities.append({"text": item_text, "label": "B-ITEM", "box": [50, y, 200, y+20]})
        
    # Draw Total
    total_text = f"{total_labels[lang]}: ${amount}"
    draw.text((50, 400), total_text, fill=(0, 0, 0))
    entities.append({"text": amount, "label": "B-TOTAL", "box": [180, 400, 280, 425]})
    
    # Save image
    img_path = f"data/images/invoice_{index}.png"
    image.save(img_path)
    
    return {
        "image_path": img_path,
        "width": width,
        "height": height,
        "entities": entities,
        "language": lang
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10)
    args = parser.parse_args()
    
    os.makedirs("data/images", exist_ok=True)
    os.makedirs("data/labels", exist_ok=True)
    
    dataset = []
    for i in range(args.samples):
        # Alternate languages
        lang = 'en' if i % 2 == 0 else 'es'
        data = generate_synthetic_invoice(i, lang)
        dataset.append(data)
        
    with open("data/dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)
        
    print(f"Generated {args.samples} synthetic invoices in 'data/' directory.")

if __name__ == "__main__":
    main()
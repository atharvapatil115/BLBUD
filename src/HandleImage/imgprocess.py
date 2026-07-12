from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load caption model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def extract_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')

    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def get_image_info(image_path):
    ocr_text = extract_ocr(image_path)
    caption = generate_caption(image_path)

    return {
        "ocr_text": ocr_text,
        "caption": caption
    }


# ✅ Test
result = get_image_info("sample.png")

print("OCR:\n", result["ocr_text"])
print("Caption:\n", result["caption"])

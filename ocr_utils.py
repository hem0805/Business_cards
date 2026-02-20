# import cv2
# import pytesseract
# from PIL import Image
# import easyocr
# from pdf2image import convert_from_path
# import os

# # Explicit path to Tesseract (adjust if installed elsewhere)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # Color map for bounding boxes
# COLOR_MAP = {
#     "Name": (255, 0, 0),      # Blue
#     "Email": (0, 255, 0),     # Green
#     "Phone": (0, 0, 255),     # Red
#     "Company": (255, 165, 0)  # Orange
# }

# def preprocess_image(image_path):
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.medianBlur(gray, 3)
#     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     return thresh

# def ocr_tesseract(image_path):
#     processed = preprocess_image(image_path)
#     text = pytesseract.image_to_string(processed)
#     return text

# def ocr_easyocr_with_boxes(image_path, entities):
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_path)
#     img = cv2.imread(image_path)

#     for (bbox, text, prob) in results:
#         x_min = min([point[0] for point in bbox])
#         y_min = min([point[1] for point in bbox])
#         x_max = max([point[0] for point in bbox])
#         y_max = max([point[1] for point in bbox])

#         # Match text against extracted entities
#         if any(text in e for e in entities.get("Name", [])):
#             color = COLOR_MAP["Name"]
#         elif any(text in e for e in entities.get("Email", [])):
#             color = COLOR_MAP["Email"]
#         elif any(text in e for e in entities.get("Phone", [])):
#             color = COLOR_MAP["Phone"]
#         elif any(text in e for e in entities.get("Company", [])):
#             color = COLOR_MAP["Company"]
#         else:
#             color = (128, 128, 128)  # gray for unclassified

#         cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)

#     annotated_path = os.path.join("uploads", "annotated.png")
#     cv2.imwrite(annotated_path, img)
#     return annotated_path

# def pdf_to_images(pdf_path, output_folder="uploads"):
#     pages = convert_from_path(pdf_path)
#     image_paths = []
#     for i, page in enumerate(pages):
#         image_path = os.path.join(output_folder, f"page_{i}.png")
#         page.save(image_path, "PNG")
#         image_paths.append(image_path)
#     return image_paths



########--------------------- Tesseract based OCR Bounding boxes

import cv2
import pytesseract
from pdf2image import convert_from_path
import os
import base64

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

COLOR_MAP = {
    "Name": (255, 0, 0),      # Blue
    "Email": (0, 255, 0),     # Green
    "Phone": (0, 0, 255),     # Red
    "Company": (255, 165, 0)  # Orange
}

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def ocr_tesseract(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)
    return text

def ocr_tesseract_with_boxes(image_path, entities):
    img = cv2.imread(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]

            if text in entities.get("Name", []):
                color, label = COLOR_MAP["Name"], "Name"
            elif text in entities.get("Email", []):
                color, label = COLOR_MAP["Email"], "Email"
            elif text in entities.get("Phone", []):
                color, label = COLOR_MAP["Phone"], "Phone"
            elif text in entities.get("Company", []):
                color, label = COLOR_MAP["Company"], "Company"
            else:
                color, label = (128, 128, 128), ""

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            if label:
                cv2.putText(img, label, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Convert annotated image to Base64 string
    _, buffer = cv2.imencode('.png', img)
    encoded = base64.b64encode(buffer).decode('utf-8')
    return encoded

from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_folder="uploads", poppler_path=r'C:\Users\hemna\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin'):
    """
    Convert a PDF into images using pdf2image.
    If poppler_path is provided, it will use that instead of relying on PATH.
    """
    if poppler_path:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    else:
        pages = convert_from_path(pdf_path)

    image_paths = []
    for i, page in enumerate(pages):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        page.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths
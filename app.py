# from flask import Flask, request, render_template
# import os, base64
# from io import BytesIO
# from PIL import Image
# from ocr_utils import ocr_tesseract, pdf_to_images, ocr_tesseract_with_boxes
# from entity_extraction import extract_entities

# app = Flask(__name__, template_folder="templates")

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     extracted_text, entities, annotated_base64, uploaded_base64 = None, None, None, None

#     if request.method == "POST":
#         file_path = None

#         # Camera capture
#         if "camera_image" in request.form and request.form["camera_image"]:
#             try:
#                 data = request.form["camera_image"].split(",")[1]
#                 img_bytes = base64.b64decode(data)
#                 img = Image.open(BytesIO(img_bytes))
#                 file_path = os.path.join(UPLOAD_FOLDER, "camera_capture.png")
#                 img.save(file_path)

#                 # Persist captured image as base64
#                 uploaded_base64 = base64.b64encode(img_bytes).decode("utf-8")
#             except Exception as e:
#                 extracted_text = f"Camera capture error: {str(e)}"

#         # File upload
#         elif "file" in request.files and request.files["file"]:
#             file = request.files["file"]
#             file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#             file.save(file_path)

#             # Persist uploaded image as base64 (only if not PDF)
#             if not file_path.lower().endswith(".pdf"):
#                 with open(file_path, "rb") as f:
#                     uploaded_base64 = base64.b64encode(f.read()).decode("utf-8")

#         # OCR + entity extraction
#         if file_path:
#             if file_path.lower().endswith(".pdf"):
#                 image_paths = pdf_to_images(file_path, UPLOAD_FOLDER)
#                 text = ""
#                 for img_path in image_paths:
#                     text += ocr_tesseract(img_path) + "\n"
#                 extracted_text = text
#             else:
#                 extracted_text = ocr_tesseract(file_path)

#             entities = extract_entities(extracted_text)
#             annotated_base64 = ocr_tesseract_with_boxes(file_path, entities)

#     return render_template("index.html",
#                            extracted_text=extracted_text,
#                            entities=entities,
#                            annotated_base64=annotated_base64,
#                            uploaded_base64=uploaded_base64)

# if __name__ == "__main__":
#     app.run(debug=True)

import os, base64
from io import BytesIO
from flask import Flask, request, render_template
from PIL import Image
from ocr_utils import ocr_tesseract, pdf_to_images, ocr_tesseract_with_boxes
from entity_extraction import extract_entities

app = Flask(__name__, template_folder="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Optional: set Poppler path explicitly if not in PATH
POPLER_PATH = r"C:\Users\hemna\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"  # adjust if needed, or set to None

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text, entities, annotated_base64, uploaded_base64 = None, None, None, None
    pdf_results = None

    if request.method == "POST":
        file_path = None

        # Camera capture
        if "camera_image" in request.form and request.form["camera_image"]:
            try:
                data = request.form["camera_image"].split(",")[1]
                img_bytes = base64.b64decode(data)
                img = Image.open(BytesIO(img_bytes))
                file_path = os.path.join(UPLOAD_FOLDER, "camera_capture.png")
                img.save(file_path)

                uploaded_base64 = base64.b64encode(img_bytes).decode("utf-8")
            except Exception as e:
                extracted_text = f"Camera capture error: {str(e)}"

        # File upload
        elif "file" in request.files and request.files["file"]:
            file = request.files["file"]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            if not file_path.lower().endswith(".pdf"):
                with open(file_path, "rb") as f:
                    uploaded_base64 = base64.b64encode(f.read()).decode("utf-8")

        # OCR + entity extraction
        if file_path:
            if file_path.lower().endswith(".pdf"):
                image_paths = pdf_to_images(file_path, UPLOAD_FOLDER, poppler_path=POPLER_PATH)
                pdf_results = {}
                for i, img_path in enumerate(image_paths, start=1):
                    text = ocr_tesseract(img_path)
                    page_entities = extract_entities(text)
                    page_annotated = ocr_tesseract_with_boxes(img_path, page_entities)

                    # Original page preview
                    with open(img_path, "rb") as f:
                        page_uploaded = base64.b64encode(f.read()).decode("utf-8")

                    pdf_results[f"Page {i}"] = {
                        "text": text,
                        "entities": page_entities,
                        "annotated_base64": page_annotated,
                        "uploaded_base64": page_uploaded
                    }
            else:
                extracted_text = ocr_tesseract(file_path)
                entities = extract_entities(extracted_text)
                annotated_base64 = ocr_tesseract_with_boxes(file_path, entities)

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        entities=entities,
        annotated_base64=annotated_base64,
        uploaded_base64=uploaded_base64,
        pdf_results=pdf_results
    )

if __name__ == "__main__":
    app.run(debug=True)
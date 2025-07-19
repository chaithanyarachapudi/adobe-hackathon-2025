import fitz  # PyMuPDF
import os
import json
import argparse
from langdetect import detect
import pytesseract
from pdf2image import convert_from_path

# Optional: Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_text_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='eng+hin+tel') + "\n"
    return text

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)

    # 1. Try metadata title
    metadata_title = doc.metadata.get("title", "").strip()

    # 2. Fallback: find first large text from page 1
    fallback_title = ""
    try:
        page0 = doc[0]
        blocks = page0.get_text("dict")["blocks"]
        spans = []
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)
                    if len(text) > 5:
                        spans.append((size, text))
        if spans:
            spans.sort(reverse=True)
            fallback_title = spans[0][1]
    except:
        fallback_title = ""

    # 3. Choose best title
    if (
        not metadata_title
        or "Microsoft Word" in metadata_title
        or metadata_title.lower().startswith("file")
    ):
        pdf_title = fallback_title or os.path.splitext(os.path.basename(pdf_path))[0]
    else:
        pdf_title = metadata_title

    # 4. Check for empty text (e.g. scanned PDF)
    full_text = "".join([p.get_text() for p in doc])
    if len(full_text.strip()) < 20:
        ocr_text = extract_text_ocr(pdf_path)
        headings = []
        for line in ocr_text.split("\n"):
            line = line.strip()
            if len(line) > 8:
                headings.append({"level": "H1", "text": line, "page": 1})
        return {"title": pdf_title.strip(), "outline": headings}

    # 5. Font-size / layout based heading extraction
    all_headings = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = span.get("size", 0)
                    if not text or len(text) < 3:
                        continue

                    # Language filtering (English/Hindi/Telugu)
                    lang = detect_language(text)
                    if lang not in ['en', 'hi', 'te']:
                        continue

                    # Layout-based enhancements
                    font_flags = span.get("flags", 0)
                    is_bold = font_flags & 2 != 0
                    is_centered = abs(span["origin"][0] - (page.rect.width / 2)) < 100

                    if size >= 18 or is_bold or is_centered:
                        level = "H1" if size >= 18 or is_centered else "H2" if size >= 14 else "H3"
                        all_headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

    return {
        "title": pdf_title.strip(),
        "outline": all_headings
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing PDF files")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save JSON outputs")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            data = extract_headings(pdf_path)
            output_path = os.path.join(output_dir, file.replace(".pdf", "_output.json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()

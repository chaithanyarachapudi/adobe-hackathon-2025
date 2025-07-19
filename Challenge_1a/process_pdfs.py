import fitz  # PyMuPDF
import os
import json

def extract_headings(pdf_path):
    import fitz
    import os

    doc = fitz.open(pdf_path)
    all_headings = []

    # Step 1: Use file name as fallback title
    pdf_title = os.path.splitext(os.path.basename(pdf_path))[0]

    found_title = False  # for first heading as title

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                font_size = 0

                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) < 2:
                        continue
                    if all(c in "-–_=*" for c in text):  # skip dashed lines
                        continue

                    line_text += text + " "
                    font_size = max(font_size, span["size"])

                line_text = line_text.strip()
                if not line_text or len(line_text) < 3:
                    continue

                # Decide level
                if font_size >= 18:
                    level = "H1"
                elif font_size >= 14:
                    level = "H2"
                elif font_size >= 12:
                    level = "H3"
                else:
                    continue

                # Save first H1 as title
                if not found_title and level == "H1":
                    pdf_title = line_text
                    found_title = True

                all_headings.append({
                    "level": level,
                    "text": line_text,
                    "page": page_num
                })

    return {
        "title": pdf_title,
        "outline": all_headings
    }


def main():
    input_dir = "./sample_dataset"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            data = extract_headings(pdf_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

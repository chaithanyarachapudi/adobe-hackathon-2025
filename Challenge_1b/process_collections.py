import os
import json
import fitz  # PyMuPDF

def extract_relevant_content(pdf_path, query):
    doc = fitz.open(pdf_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if query.lower() in text.lower():
            results.append({
                "pdf": os.path.basename(pdf_path),
                "page": page_num,
                "text": text.strip()[:800]  # truncate if needed
            })

    return results

def process_collection(collection_path):
    input_json = os.path.join(collection_path, "challenge1b_input.json")
    output_json = os.path.join(collection_path, "challenge1b_output.json")
    pdf_folder = os.path.join(collection_path, "PDFs")

    with open(input_json, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona = input_data.get("persona", "")
    goal = input_data.get("goal", "")

    all_results = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            matches = extract_relevant_content(pdf_path, goal)
            all_results.extend(matches)

    output_data = {
        "persona": persona,
        "goal": goal,
        "results": all_results
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

# 🏁 MAIN EXECUTION
if __name__ == "__main__":
    for collection in ["Collection 1", "Collection 2", "Collection 3"]:
        print(f"🔍 Processing: {collection}")
        process_collection(collection)
        print(f"✅ Done: {collection}")

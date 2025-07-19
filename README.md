

## ✅ Challenge 1A - PDF Heading Structure Extraction

### 📄 Problem Statement

Extract structured heading outlines (H1, H2, H3) from each page of a PDF and return them in a JSON format.


### 🗂️ Folder Structure

Challenge_1a/
├── sample_dataset/
│   ├── file01.pdf
│   └── file01_output.json
├── process_pdfs.py
├── requirements.txt
└── README.md

### ⚙️ Setup Instructions

1. **Clone Repo & Navigate:**

   git clone https://github.com/chaithanyarachpudi/adobe-hackathon-2025.git
   cd adobe-hackathon-2025/Challenge_1a


2. **Install Requirements:**

   pip install -r requirements.txt


3. **Run the Extractor:**

   python process_pdfs.py --input_dir sample_dataset --output_dir output

   
### 📥 Input

PDFs stored in the `sample_dataset/` folder.


### 📤 Output

For each `.pdf`, a corresponding `_output.json` file is created in the same folder.

**Example Output:**

{
  "title": "Application form for grant of LTC advance",
  "outline": [
    {
      "level": "H1",
      "text": "Section A: Personal Details",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Name and Designation",
      "page": 1
    }
  ]
}

### 🔧 Heuristics Used

* Font size-based classification:

  * H1: size ≥ 18
  * H2: size ≥ 14
  * H3: size ≥ 12
* Optionally, boldness and position can be used for enhancement.
from pdfminer.high_level import extract_text
import fitz

# pdf_file = '../civil_code/source.pdf'
# doc = fitz.open(pdf_file)

#
# # Extracting text from all pages
# all_text = []
# for page_num in range(len(doc)):
#     page = doc[page_num]
#     text = page.get_text()
#     all_text.append([page_num + 1, text])
#     print(text)
# # text = extract_text(pdf_file)
# # print(text)

import os

from src.utils.utils import get_project_root

for dir_name in os.listdir():
    pdf_file_path = get_project_root() / "documents" / "legal_acts" /"batch" / dir_name / "source.pdf"
    doc = fitz.open(pdf_file_path)
    all_text = []
    for page in doc:
        # page = doc[page_num]
        text = page.get_text()
        # all_text.append([page_num + 1, text])
        # print(text)
    "/n".join(all_text)
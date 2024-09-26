import fitz
import os
from src.utils.utils import get_project_root

if __name__ == "__main__":
    list_of_directories = [directory for directory in os.listdir() if directory[-3:] != ".py"]
    print(list_of_directories)
    # list_of_directories = ["penal_code", "labor_code"]
    for dir_name in list_of_directories:
        dir_path = get_project_root() / "documents" / "legal_acts" /"batch" / dir_name
        pdf_file_path = dir_path / "source.pdf"
        txt_file_path = dir_path / "source.txt"
        doc = fitz.open(pdf_file_path)
        text_pages = []
        for page in doc:
            text = page.get_text()
            text_pages.append(text)

        with open(txt_file_path,"w", encoding="UTF-8") as f:
            f.write("\n".join(text_pages))


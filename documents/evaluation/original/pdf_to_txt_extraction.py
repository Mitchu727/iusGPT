import fitz
import os
from src.utils.utils import get_project_root

if __name__ == "__main__":
    # list_of_directories = [directory for directory in os.listdir() if directory[-3:] != ".py"]
    list_of_directories = ["egzamin_wstepny_adwokacki_radcowski_2024", "egzamin_wstepny_komorniczy_2024", "egzamin_wstepny_notarialny_2024"]
    # list_of_directories = ["egzamin_wstepny_adwokacki_radcowski_2024"]
    print(list_of_directories)
    for dir_name in list_of_directories:
        dir_path = get_project_root() / "documents" / "evaluation"/ "original" / dir_name
        questions_pdf_file_path = dir_path / "questions.pdf"
        questions_txt_file_path = dir_path / "questions.txt"
        doc = fitz.open(questions_pdf_file_path)
        text_pages = []
        for page in doc:
            text = page.get_text()
            text_pages.append(text)

        with open(questions_txt_file_path, "w", encoding="UTF-8") as f:
            f.write("\n".join(text_pages))
            
        answers_pdf_file_path = dir_path / "answers.pdf"
        answers_txt_file_path = dir_path / "answers.txt"
        doc = fitz.open(answers_pdf_file_path)
        text_pages = []
        for page in doc:
            text = page.get_text()
            text_pages.append(text)

        with open(answers_txt_file_path, "w", encoding="UTF-8") as f:
            f.write("\n".join(text_pages))



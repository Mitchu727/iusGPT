import json
import re
import fitz
from src.utils.utils import get_project_root, get_original_questions_list_directories


def extract_from_pdf_to_txt(list_of_directories):
    for dir_name in list_of_directories:
        dir_path = get_project_root() / "documents" / "evaluation" / "original" / dir_name
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


def extract_questions(list_of_directories):
    for dir_path in list_of_directories:
        # dir_path = get_project_root() / "documents" / "evaluation" / "original" / dir_name
        questions_txt_file_path = dir_path / "questions.txt"
        questions_json_file_path = dir_path / "questions.json"

        with open(questions_txt_file_path, "r", encoding="utf-8") as f:
            questions_raw = f.read()
        questions_raw = re.sub(r"((.|\n)*?)(1\. \nZgodnie)", r'\3', questions_raw, count=1)
        questions_raw = re.sub(r"\n(?!(A\.|B\.|C\.|[0-9]+\.))", " ", questions_raw)
        questions_raw = re.sub(r"([0-9]+)* *EGZAMIN WSTĘPNY DLA KANDYDATÓW NA APLIKANTÓW.*", "", questions_raw)
        questions_raw = re.sub(r" +", " ", questions_raw)

        questions_lines = questions_raw.split("\n")

        questions = []
        for i in range(150):
            question_index_offset = len(str(i + 1))

            question = {
                "index": i + 1,
                "question": questions_lines[4 * i][question_index_offset + 2:],
                "a": questions_lines[4 * i + 1][3:-1],
                "b": questions_lines[4 * i + 2][3:-1],
                "c": questions_lines[4 * i + 3][3:-1]
            }

            questions.append(question)

        with open(questions_json_file_path, "w") as f:
            json.dump(questions, f)


def extract_answers(list_of_directories):
    for dir_path in list_of_directories:
        # dir_path = get_project_root() / "documents" / "evaluation" / "original" / dir_name
        answers_txt_file_path = dir_path / "answers.txt"
        answers_json_file_path = dir_path / "answers.json"
        with open(answers_txt_file_path, "r", encoding="utf-8") as f:
            answers_raw = f.read()
        answers_raw = re.sub(r"(.|\n)*?1\.", "1.", answers_raw, count=1)
        answers_raw = re.sub(r"\n[0-9]+ *\n", "\n", answers_raw)
        answers_raw = re.sub(r"\n(?![0-9]+)", " ", answers_raw)
        answers_raw = re.sub(r"Aart\.", "A art.", answers_raw)
        answers_raw = re.sub(r"Bart\.", "B art.", answers_raw)
        answers_raw = re.sub(r"Cart\.", "C art.", answers_raw)
        answers_raw = re.sub(r" +", " ", answers_raw)

        print(answers_raw)

        answers_rows = answers_raw.split("\n")

        answers = []
        for i, answers_row in enumerate(answers_rows):
            question_index_offset = len(str(i + 1))

            answer = {
                "index": i + 1,
                "answer": answers_row[question_index_offset + 2],
                "context": answers_row[question_index_offset + 4:],
            }
            answers.append(answer)

        with open(answers_json_file_path, "w") as f:
            json.dump(answers, f)


if __name__ == "__main__":
    list_of_directories = get_original_questions_list_directories()
    extract_from_pdf_to_txt(list_of_directories)
    extract_questions(list_of_directories)
    extract_answers(list_of_directories)


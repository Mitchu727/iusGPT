import re
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def get_runs_directory() -> Path:
    return get_project_root() / "runs"


def get_legal_acts_directory() -> Path:
    return get_project_root() / "documents" / "legal_acts"


def get_legal_act_json_path(legal_act) -> Path:
    return get_project_root() / "documents" / "legal_acts" / legal_act / "source.json"


def extract_id_from_article_content(article_text):
    try:
        return re.search(r"Art\. [0-9a-zł]+\.", article_text).group()
    except Exception as e:
        print(article_text)
        raise Exception


def get_example_question() -> dict:
    return {
        "index": 30,
        "question": "Zgodnie z Kodeksem cywilnym, ograniczoną zdolność do czynności prawnych mają:",
        "a": "osoby ubezwłasnowolnione całkowicie",
        "b": "małoletni, którzy ukończyli lat dziesięć, oraz osoby ubezwłasnowolnione całkowicie",
        "c": "małoletni, którzy ukończyli lat trzynaście, jeżeli nie zostali ubezwłasnowolnieni całkowicie, oraz osoby ubezwłasnowolnione częściowo"
    }

def get_hard_example_question() -> dict:
    return {
        "index": 37,
        "question": "Zgodnie z Kodeksem cywilnym, własność nieruchomości:",
        "a": "nie może być przeniesiona pod warunkiem ani z zastrzeżeniem terminu",
        "b": "nie może być przeniesiona pod warunkiem, ale może być przeniesiona z  zastrzeżeniem terminu",
        "c": "może być przeniesiona pod warunkiem, ale nie może być przeniesiona z  zastrzeżeniem terminu"
    }


def format_question(question_dict):
    return """Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}
            """.format(
        question=question_dict["question"],
        answer_a=question_dict["a"],
        answer_b=question_dict["b"],
        answer_c=question_dict["c"]
    )

def format_answer(answer_dict):
    return f"{answer_dict['answer']}, context: {answer_dict['context']}"


def convert_string_to_list(list_as_string):
    return list_as_string[1:-1].split(", ")
import re
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

def get_runs_directory() -> Path:
    return get_project_root() / "runs"

def extract_id_from_article_content(article_content):
    result = re.search("Art. [0-9]*.", article_content)
    return result.group()

def get_example_question() -> dict:
    return {
        "index": 30,
        "question": "Zgodnie z Kodeksem cywilnym, ograniczoną zdolność do czynności prawnych mają:",
        "a": "osoby ubezwłasnowolnione całkowicie",
        "b": "małoletni, którzy ukończyli lat dziesięć, oraz osoby ubezwłasnowolnione całkowicie",
        "c": "małoletni, którzy ukończyli lat trzynaście, jeżeli nie zostali ubezwłasnowolnieni całkowicie, oraz osoby ubezwłasnowolnione częściowo"
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
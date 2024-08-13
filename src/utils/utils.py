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
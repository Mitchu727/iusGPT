from src.secrets import OPEN_API_KEY

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": OPEN_API_KEY,
        "base_url": "https://api.openai.com/v1",
    }
]

llm_config = {
    "config_list": config_list,
}

PROBLEM = """
        Stan faktyczny:
        Błażej ma 30 lat i nie jest ubezwłasnowolniony
        Pytanie:
        Odpowiedz czy posiada pełną zdolność do czynności prawnych.
    """
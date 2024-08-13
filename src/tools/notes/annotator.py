import json
from src.utils.utils import get_project_root

civil_articles_path = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"


class Annotator:
    system_prompt = """
        You are an expert in extracting information from legal regulations. Your task is to create concise study notes by identifying and listing key topics from articles of the civil code. You will be provided with a specific regulation. Your response should include a list of key topics or terms that would help in quickly identifying the article's subject matter later.
        Instructions:
    
        Read the provided regulation carefully to understand its content.
        Identify key legal terms and concepts mentioned in the regulation. These should be the main topics or points of interest in the article.
        List these key topics in your response, separated by commas. Use short phrases or keywords that would help in recalling the content of the article later.
    
        Example:
    
        Regulation:
    
        Art. 17. Z zastrzeżeniem wyjątków w ustawie przewidzianych, do ważności czynności prawnej, przez którą osoba ograniczona w zdolności do czynności prawnych zaciąga zobowiązanie lub rozporządza swoim prawem, potrzebna jest zgoda jej przedstawiciela ustawowego.
    
        Answer:
    
        ważność czynności prawnej, osoba ograniczona w zdolności do czynności prawnych, przedstawiciel ustawowy
        """

    def __init__(self):
        pass

if __name__ == '__main__':
    with open(civil_articles_path, "r") as f:
        articles = json.load(f)

    for article in articles:
        print(article['content'])
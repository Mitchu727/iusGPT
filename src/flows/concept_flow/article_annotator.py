import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


from src.utils.utils import get_project_root, extract_id_from_article_content
import src.secret

civil_articles_path = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"
output_file_path = "civil_code_annotated.txt"

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


    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{article}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def annotate_article(self, article_content):
        return self.chain.invoke({"article": article_content})


if __name__ == '__main__':
    with open(civil_articles_path, "r") as f:
        articles = json.load(f)

    annotator = Annotator()
    annotations = []
    for article in articles:
        annotation = annotator.annotate_article(article['content'])
        print("=======ARTICLE=======")
        print(article['content'])
        article_id = extract_id_from_article_content(article['content'])
        article_with_annotation = f"{article_id} {annotation}"

        print("=======ANNOTATION=======")
        print(article_with_annotation)
        print()

        annotations.append(article_with_annotation)

    text = "\n".join(annotations)

    with open(output_file_path, "w") as f:
        f.write(text)

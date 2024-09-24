import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


from src.utils.utils import get_project_root, extract_id_from_article_content
import src.secrets

civil_articles_path = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"
output_file_path = "civil_code_summarized.txt"

class Annotator:
    system_prompt = """
        You are an expert in extracting information from legal regulations.
        You will be provided with a group of specific regulations from Polish Civil Code.
        You have to create a short description of this group so that a person searching for a specific topic can easily find articles related to it.
        
        Example:
    
        Regulations:
            Art. 1. Kodeks niniejszy reguluje stosunki cywilnoprawne między osobami
        fizycznymi i osobami prawnymi.
        
        Art. 3. Ustawa nie ma mocy wstecznej, chyba że to wynika z jej brzmienia lub
        celu.
        
        Art. 5. Nie można czynić ze swego prawa użytku, który by był sprzeczny ze
        społeczno-gospodarczym przeznaczeniem tego prawa lub z zasadami współżycia
        społecznego. Takie działanie lub zaniechanie uprawnionego nie jest uważane za
        wykonywanie prawa i nie korzysta z ochrony.
        
        Art. 6. Ciężar udowodnienia faktu spoczywa na osobie, która z faktu tego
        wywodzi skutki prawne.
        
        Art. 7. Jeżeli ustawa uzależnia skutki prawne od dobrej lub złej wiary,
        domniemywa się istnienie dobrej wiary.
        
        Answer:
        Przepisy wstępne kodeksu cywilnego, w których określono ogólne zasady dotyczące stosowania przepisów prawa cywilnego. Zawiera definicje podstawowych pojęć, zasadę niedziałania prawa wstecz, oraz zasady korzystania z praw i udowadniania faktów.
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

    annotator = Annotator("gpt-4o-mini")

    chunks = {}
    for article in articles:
        chunk_id = f"{article['book'][1:].replace(' ', '_')}-{article['title'].replace(' ', '_')}-{article['section'].replace(' ', '_')}-{article['chapter'].replace(' ', '_')}"
        if chunk_id not in chunks.keys():
            chunks[chunk_id] = [article['content']]
        else:
            chunks[chunk_id].append(article['content'])
    # chunk_contents = ["\n".join(chunk) for chunk in chunks.values()]
    # chunk_contents = ["\n".join(chunk) for chunk in chunks.values()]
    text_parts = []
    for chunk in list(chunks.values()):
        chunk_content = "\n".join(chunk)
        first_chunk_article = extract_id_from_article_content(chunk[0])
        last_chunk_article = extract_id_from_article_content(chunk[-1])
        chunk_id = f"{first_chunk_article}-{last_chunk_article}"
        chunk_description = annotator.annotate_article(chunk)
        print(chunk_id)
        print(chunk_description)
        text_parts.append(chunk_id)
        text_parts.append(chunk_description)

    text = "\n".join(text_parts)
    with open(output_file_path, "w") as f:
        f.write(text)

    # annotator = Annotator()
    # annotations = []
    # for article in articles:
    #     annotation = annotator.annotate_article(article['content'])
    #     print("=======ARTICLE=======")
    #     print(article['content'])
    #     article_id = extract_id_from_article_content(article['content'])
    #     article_with_annotation = f"{article_id} {annotation}"
    #
    #     print("=======ANNOTATION=======")
    #     print(article_with_annotation)
    #     print()
    #
    #     annotations.append(article_with_annotation)
    #
    # text = "\n".join(annotations)
    #
    # with open(output_file_path, "w") as f:
    #     f.write(text)

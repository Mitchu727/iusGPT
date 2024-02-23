from src.article_collection.chroma_db_collection import get_civil_code_collection
from openai import OpenAI


class ArticleEnricherAgent:
    def __init__(self):
        self.chroma_collection = get_civil_code_collection()
        self.open_ai_client = OpenAI()

    def enrich_with_articles(self, query, number_of_fetched_documents):
        results = self.chroma_collection.query(query_texts=[query], n_results=number_of_fetched_documents)
        articles_list = results['documents'][0]
        articles = "".join(articles_list)
        # print(articles)
        prompt = prompt_wrapper(query, articles)
        response = self.open_ai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content


def prompt_wrapper(query, articles):
    return f"""
Dane jest następujące pytanie:
{query}

I następujące przepisy prawne:
{articles}

Twoim zadaniem jest wybrać z podanych artykułów te, które mogą być przydatne i uzupełnić nimi pytanie.
Udziel odpowiedzi w formie:
<pytanie>
<artykuł>
"""
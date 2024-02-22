from src.article_collection.chroma_db_collection import get_civil_code_collection

from src.secrets import OPEN_API_KEY
import os
import chromadb
from openai import OpenAI

QUERY = "Czym jest gospodarstwo rolne?"

def prompt_wrapper(query, articles):
    return f"""
Dane jest następujące pytanie:
{query}

I następujące przepisy prawne
{articles}

Twoim zadaniem jest wybrać z podanych artykułów te, które mogą być przydatne i uzupełnić nimi pytanie.
Udziel odpowiedzi w formie:
<zagadnienie>
<artykuł>
"""

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

if __name__ == "__main__":
    chroma_collection = get_civil_code_collection()
    results = chroma_collection.query(query_texts=[QUERY], n_results=10)
    articles_list = results['documents'][0]
    articles = "".join(articles_list)
    prompt = prompt_wrapper(QUERY, articles)
    print(prompt)
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(response.choices[0].message.content)

    # print(response)
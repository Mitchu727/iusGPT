from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import json

from src.utils.utils import get_project_root

default_articles_source = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"


def load_articles(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
    documents = []
    for article in articles:
        # document = Document(page_content=article["content"].replace("\n", " "))
        documents.append(article["content"].replace("\n", " "))
    return documents

# def create_chroma_retriever(docs, k=5):
#     model_name = "sdadas/mmlw-roberta-base"
#     # model_name = "BAAI/bge-multilingual-gemma2"
#     embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
#     db = Chroma.from_documents(docs, embedding_function)
#     print("There are", db._collection.count(), "documents in the collection")
#     retriever = db.as_retriever(search_kwargs={"k": k})
#     return retriever

def score_overlap(article_part, phrase):
    counter = 0
    for i in range(0, len(article_part)):
        if article_part[i] == phrase[i]:
            counter += 1
    return counter


def score_by_phrase(article, phrase):
    max_score = 0
    for i in range(0, len(article)-len(phrase)):
        analyzed_part = article[i:i+len(phrase)]
        part_score = score_overlap(analyzed_part, phrase)
        if part_score > max_score:
            max_score = part_score
    return max_score

def sort_list_by_another(list_to_sort, another_list):

    zipped_pairs = zip(another_list, list_to_sort)

    z = [x for _, x in sorted(zipped_pairs, reverse=True)]

    return z
        # for j in range(0, len(phrase)):
        # print(analyzed_part)

def retrieve_articles(phrase, k):
    docs = load_articles()
    article_scores = []
    for doc in docs:
        article_scores.append(score_by_phrase(doc, phrase))
    return sort_list_by_another(docs, article_scores)[:k]

if __name__ == "__main__":
    print(retrieve_articles("ubezwłasnowolnienie", 10))


    # retriever = create_chroma_retriever(docs)
    # print(retriever.invoke("ubezwłasnowolnienie"))
    # "Zgodnie z art. 999 Kodeksu cywilnego, fundacja ustanowiona w testamencie przez spadkodawcę może być spadkobiercą, jeżeli zostanie wpisana do rejestru fundacji w ciągu dwóch lat od otwarcia spadku."
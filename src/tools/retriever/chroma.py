from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import json

from src.utils.utils import get_project_root

default_articles_source = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"


def load_articles_as_documents(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
    documents = []
    for article in articles:
        document = Document(page_content=article["content"].replace("\n", " "))
        documents.append(document)
    return documents

def create_chroma_retriever(docs, k=5):
    model_name = "sdadas/mmlw-roberta-base"
    # model_name = "BAAI/bge-multilingual-gemma2"
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    db = Chroma.from_documents(docs, embedding_function)
    print("There are", db._collection.count(), "documents in the collection")
    retriever = db.as_retriever(search_kwargs={"k": k})
    return retriever

if __name__ == "__main__":
    docs = load_articles_as_documents()
    retriever = create_chroma_retriever(docs)
    print(retriever.invoke("zapytanie: ubezwłasnowolnienie"))
    # "Zgodnie z art. 999 Kodeksu cywilnego, fundacja ustanowiona w testamencie przez spadkodawcę może być spadkobiercą, jeżeli zostanie wpisana do rejestru fundacji w ciągu dwóch lat od otwarcia spadku."
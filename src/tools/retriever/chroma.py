from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import json

from src.utils.utils import get_project_root

default_articles_source = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"


def load_articles(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
        return [article["content"].replace("\n", " ") for article in articles]


def create_chroma_retriever(docs):
    model_name = "sdadas/mmlw-roberta-base"
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    db = Chroma.from_documents(docs, embedding_function)
    print("There are", db._collection.count(), "documents in the collection")
    retriever = db.as_retriever(search_kwargs={"k": 20})
    return retriever


if __name__ == "__main__":
    docs = load_articles()
    create_chroma_retriever(docs)

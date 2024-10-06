from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import json

from src.utils.utils import get_project_root, get_legal_act_json_path, get_chroma_path

default_articles_source = get_project_root() / "documents" / "legal_acts" / "batch" / "civil_code" / "source.json"


def load_articles_as_documents(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
    documents = []
    for article in articles:
        document = Document(page_content=article["content"].replace("\n", " "))
        documents.append(document)
    return documents


def create_chroma_retriever(docs, name="civil_code", k=5, create_new_instance=True):
    persist_directory = str(get_chroma_path())

    model_name = "sdadas/mmlw-roberta-large"
    # model_name = "BAAI/bge-multilingual-gemma2"
    embedding_function = HuggingFaceEmbeddings(model_name=model_name)
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function, collection_name=name)
    if create_new_instance:
        db.delete_collection()
        db = Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory, collection_name=name)


    print(f"There are {db._collection.count()}, documents in the collection: {name}")
    retriever = db.as_retriever(search_kwargs={"k": k})
    return retriever


if __name__ == "__main__":
    docs = load_articles_as_documents(get_legal_act_json_path("civil_code"))
    docs_v2 = load_articles_as_documents(get_legal_act_json_path("penal_code"))
    retriever = create_chroma_retriever(docs, "civil_code", k=100, create_new_instance=False)
    # retriever2 = create_chroma_retriever(docs_v2, "penal_code")
    results = retriever.invoke("zapytanie: Wyszukaj artykuły z kodeksu cywilnego, które dotyczą zakazu skracania lub przedłużania terminów przedawnienia ('terminy przedawnienia') przez czynności prawne.")
    for result in results:
        print(result.page_content)
    # print(retriever2.invoke("zapytanie: kradzież"))
    # "Zgodnie z art. 999 Kodeksu cywilnego, fundacja ustanowiona w testamencie przez spadkodawcę może być spadkobiercą, jeżeli zostanie wpisana do rejestru fundacji w ciągu dwóch lat od otwarcia spadku."
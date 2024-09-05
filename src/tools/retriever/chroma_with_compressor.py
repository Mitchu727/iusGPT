from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document, compressor
import src.secrets
import json

from langchain_openai import ChatOpenAI

from src.tools.retriever.chroma import create_chroma_retriever
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

def create_chroma_with_compressor_retriever(docs, k=5, model="gpt-3.5-turbo-0125"):
    llm = ChatOpenAI(model=model, temperature=0)
    model_name = "sdadas/mmlw-roberta-base"
    # model_name = "BAAI/bge-multilingual-gemma2"
    embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
    db = Chroma.from_documents(docs, embedding_function)
    print("There are", db._collection.count(), "documents in the collection")
    retriever = db.as_retriever(search_kwargs={"k": k})
    llm_filter = LLMChainFilter.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=llm_filter, base_retriever=retriever
    )
    return compression_retriever


# if __name__ == "__main__":
#     docs = load_articles_as_documents()
#     retriever = create_chroma_with_compressor_retriever(docs, k=10)
#     print(retriever.invoke("ubezwłasnowolnienie"))
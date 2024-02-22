from llama_index.vector_stores import ChromaVectorStore
from src.article_collection.chroma_db_collection import get_civil_code_collection
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage

from src.secrets import OPEN_API_KEY
from src.article_collection.embeddings import sentence_transformer

import os

PROMPT = """
    Dane jest następujące pytanie:
    Czym jest gospodarstwo rolne?

    Twoim zadaniem jest wybrać z podanych artykułów te, które mogą być przydatne i uzupełnić nimi pytanie.
    Udziel odpowiedzi w formie:
    <zagadnienie>
    <artykuł>
"""

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

if __name__ == "__main__":
    print(len(sentence_transformer(PROMPT)))
    chroma_collection = get_civil_code_collection()
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection, dimension=384)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=sentence_transformer,
        dimension = 384
    )

    query_engine = index.as_query_engine()
    response = query_engine.query(PROMPT)

    # print(response)
# BASED ON https://stackoverflow.com/questions/76372225/use-llamaindex-with-different-embeddings-model


import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

import logging
import sys
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext, StorageContext
from icecream import ic
import llama_index
from llama_index.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.indices.vector_store.retrievers import VectorIndexRetriever
from llama_index import load_index_from_storage

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
query = "What did the author do growing up?"
# query = "Jaka jest definicja nieruchomości zgodnie z polskim kodeksem cywilnym?"

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "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"

    # Initialize embedding model
    embed_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    embed_model = "local"
    service_context_embeddings = ServiceContext.from_defaults(embed_model=embed_model)

    # check if storage already exists
    if not os.path.exists("../src/storage"):
        # load the documents and create the index
        documents = SimpleDirectoryReader("../smallData").load_data()
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist()
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir="../src/storage")
        index = load_index_from_storage(storage_context)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=10)
    nodes = retriever.retrieve(query)
    ic(nodes)

    # Initialize LLM service context and response synthesizer
    response_synthesizer = llama_index.response_synthesizers.get_response_synthesizer(
        response_mode="compact",
        use_async=False,
        streaming=False,
    )

    # Initialize and run query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )

    query_engine = index.as_query_engine()
    # response = query_engine.query("Jaka jest definicja nieruchomości zgodnie z polskim kodeksem cywilnym?")
    response = query_engine.query()
    print(response)
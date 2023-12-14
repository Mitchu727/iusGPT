import os
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import logging
import sys
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage
from llama_index.embeddings import LangchainEmbedding

from src.secrets import OPEN_API_KEY

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

    # # check if storage already exists
    # if not os.path.exists("./storage"):
    #     # load the documents and create the index
    #     documents = SimpleDirectoryReader("../smallData").load_data()
    #     index = VectorStoreIndex.from_documents(documents)
    #     # store it for later
    #     index.storage_context.persist()
    # else:
    #     # load the existing index
    #     storage_context = StorageContext.from_defaults(persist_dir="./storage")
    #     index = load_index_from_storage(storage_context)

    # Load in a specific embedding model
    embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))

    # Create a service context with the custom embedding model
    service_context = ServiceContext.from_defaults(embed_model=embed_model)

    if not os.path.exists("./storage"):
        documents = SimpleDirectoryReader("../documents/civilCodeTxtReducted").load_data()
        # Load in a specific embedding model
        embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))

        # Create a service context with the custom embedding model
        service_context = ServiceContext.from_defaults(embed_model=embed_model)

        # Create an index using the service context
        new_index = VectorStoreIndex.from_documents(
            documents,
            service_context=service_context,
        )

        new_index.storage_context.persist()
    else:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        new_index = load_index_from_storage(storage_context, service_context=service_context)

    query_engine = new_index.as_query_engine()
    # response = query_engine.query("Komu przysługuje własność stanowiąca mienie państwowe?")
    # response = query_engine.query("Czy gospodarstwe rolne może składać się z samego inwentarza? Odpowiedz dlaczego i przytocz właściwy przepis")
    response = query_engine.query("Czy gospodarstwo rolne może składać się z samych budynków? Odpowiedz dlaczego i przytocz właściwy przepis")
    # response = query_engine.query("What did the author do growing up?")
    print(response)
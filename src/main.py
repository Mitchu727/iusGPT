import os
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import logging
import sys
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage
from llama_index.embeddings import LangchainEmbedding

from src.secrets import OPEN_API_KEY

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

CREATE_NEW_STORAGE = True

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

    # Load in a specific embedding model
    embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2'))

    # Create a service context with the custom embedding model
    service_context = ServiceContext.from_defaults(embed_model=embed_model)

    if not os.path.exists("./storage") or CREATE_NEW_STORAGE:
        print("Tworzenie nowej bazy kontekstu")
        documents = SimpleDirectoryReader("../documents/civilCodeTxtGenerated").load_data()
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
        print("Używanie istniejącej bazy kontekstu")
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        new_index = load_index_from_storage(storage_context, service_context=service_context)

    query_engine = new_index.as_query_engine()

    response = query_engine.query("Jaka jest definicja nieruchomości? Podaj odpowiedni przepis")
    print(f"Odpowiedź systemu: {response}")
    print("Wzorcowa odpowiedź: Art. 46. § 1. Nieruchomościami są części powierzchni ziemskiej stanowiące odrębny przedmiot własności (grunty), jak również budynki trwale z gruntem związane lub części takich budynków, jeżeli na mocy przepisów szczególnych stanowią odrębny od gruntu przedmiot własności.")

    # COMMENTED TO REDUCE THE NUMBER OF REQUESTS
    response = query_engine.query("Jaka jest definicja gospodarstwa rolnego?")
    print(f"Odpowiedź systemu: {response}")
    print("Wzorcowa odpowiedź: Art. 55 3. Za gospodarstwo rolne uważa się grunty rolne wraz z gruntami leśnymi, budynkami lub ich częściami, urządzeniami i inwentarzem, jeżeli stanowią lub mogą stanowić zorganizowaną całość gospodarczą, oraz prawami związanymi z prowadzeniem gospodarstwa rolnego.")

    response = query_engine.query("Komu przysługuje własność stanowiąca mienie państwowe?")
    print(f"Odpowiedź systemu: {response}")
    print("Wzorcowa odpowiedź: Art. 44 z indeksem 1. § 1. Własność i inne prawa majątkowe, stanowiące mienie państwowe, przysługują Skarbowi Państwa albo innym państwowym osobom prawnym.")

    response = query_engine.query("Czy gospodarstwo rolne może składać się z samych budynków? Odpowiedz dlaczego i przytocz właściwy przepis")
    print(f"Odpowiedź systemu: {response}")
    print("Wzorcowa odpowiedź: Nie, przytoczenie artykułu art. 55. § 3")

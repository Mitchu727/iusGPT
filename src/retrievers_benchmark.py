import time

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.tools.retriever.search_retriever import SearchRetriever


docs = load_articles_as_documents()
vector_store_retriever = create_chroma_retriever(docs, "civil_code", k=50)
phrase_retriever = SearchRetriever(docs=docs, k=50)

print("Evaluation one starting")
start = time.time()
for i in range(1000):
    vector_store_retriever.invoke("ubezwłasnowolnienie")
end = time.time()
print("Vectorstore retriever")
print(end-start)


print("Evaluation two starting")
start = time.time()
for i in range(1000):
    phrase_retriever.invoke("ubezwłasnowolnienie")
end = time.time()
print("Search retriever")
print(end - start)

import json
from typing import List, Any

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStoreRetriever
from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever


class PrefixedRetriever(BaseRetriever):
    retriever: VectorStoreRetriever

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Sync implementations for retriever."""
        query_prefix = "zapytanie: "
        full_query = query_prefix + query
        return self.retriever.invoke(full_query)
        # return "gogo"


if __name__ == "__main__":
    docs = load_articles_as_documents()
    chroma_retriever = create_chroma_retriever(docs)
    prefixed_retriever = PrefixedRetriever(retriever=chroma_retriever)
    docs = prefixed_retriever.invoke("ubezwłasnowolnienie")
    for doc in docs:
        print(doc)
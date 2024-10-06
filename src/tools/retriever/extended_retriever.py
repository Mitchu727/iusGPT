import logging
from typing import List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.tools.retriever.prefixed_retriever import PrefixedRetriever
from src.utils.utils import get_legal_acts_list_from_directories


class ExtendedRetriever(BaseRetriever):
    retriever: BaseRetriever = None
    range: int = 5
    docs: List[Document]

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        docs_from_retriever = self.retriever.invoke(query)
        logging.debug(f"Docs returned from base_retriever: {docs_from_retriever}")
        retrieved_docs = []
        for doc_from_retriever in docs_from_retriever:
            index = self.docs.index(doc_from_retriever)
            retrieved_docs.extend(self.docs[index-self.range:index+self.range+1])
        return retrieved_docs


if __name__ == "__main__":
    docs = load_articles_as_documents()
    # chroma_retriever = create_chroma_retriever(docs, "civil_code", k=10, create_new_instance=False)
    # prefixed_retriever = PrefixedRetriever(retriever=chroma_retriever)
    # extended_retriever = ExtendedRetriever(retriever=prefixed_retriever, range=5, docs=docs)
    # retrieved_docs = extended_retriever.invoke("ubezwłasnowolnienie")
    # print(retrieved_docs)
    # print(print(len(retrieved_docs)))
import json
from typing import List, Any


from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


from src.tools.retriever.chroma import default_articles_source


def load_articles_as_documents(path=default_articles_source):
    with open(path, "r") as f:
        articles = json.load(f)
    documents = []
    for article in articles:
        document = Document(page_content=article["content"].replace("\n", " "))
        documents.append(document)
    return documents


class SearchRetriever(BaseRetriever):
    """A toy retriever that contains the top k documents that contain the user query.

    This retriever only implements the sync method _get_relevant_documents.

    If the retriever were to involve file access or network access, it could benefit
    from a native async implementation of `_aget_relevant_documents`.

    As usual, with Runnables, there's a default async implementation that's provided
    that delegates to the sync implementation running on another thread.
    """

    documents: List[Document] = load_articles_as_documents()
    """List of documents to retrieve from."""
    k: int = 10
    """Number of top results to return"""

    @staticmethod
    def score_overlap(article_part, phrase):
        counter = 0
        for i in range(0, len(article_part)):
            if article_part[i] == phrase[i]:
                counter += 1
        return counter

    @staticmethod
    def score_by_phrase(article, phrase):
        max_score = 0
        for i in range(0, len(article) - len(phrase)):
            analyzed_part = article[i:i + len(phrase)]
            part_score = SearchRetriever.score_overlap(analyzed_part, phrase)
            if part_score > max_score:
                max_score = part_score
        return max_score

    @staticmethod
    def sort_list_by_another(list_to_sort, another_list):

        list_to_sort = [doc.page_content for doc in list_to_sort]
        zipped_pairs = zip(another_list, list_to_sort)

        z = [x for _, x in sorted(zipped_pairs, reverse=True)]
        z = [Document(page_content=s) for s in z]
        return z

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Sync implementations for retriever."""
        article_scores = []
        for doc in self.documents:
            article_scores.append(self.score_by_phrase(doc.page_content, query))
        print(article_scores)
        return self.sort_list_by_another(self.documents, article_scores)[:self.k]


if __name__ == "__main__":
    retriever = SearchRetriever(k=50)

    docs = retriever.invoke("ubezwłasnowolnienie")
    # print(retriever.k)
    # print(len(docs))
    # print(len(retriever.documents))
    print(docs)
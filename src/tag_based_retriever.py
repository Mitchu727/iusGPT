import json
from typing import List, Any

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import PrivateAttr

from src.tag_determiner import TagDeterminer


class TagBasedRetriever(BaseRetriever):
    tag_determiner: TagDeterminer = PrivateAttr(True)
    articles: List[dict] = PrivateAttr(True)
    tags: List[str] = PrivateAttr(True)
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        articles_path = "../documents/civilCodeSplitted/articles_tagged.json"
        tag_path = "../documents/tags.json"
        self.tag_determiner = TagDeterminer()
        with open(tag_path, "r") as f:
            self.tags = json.load(f)
        with open(articles_path, "r") as f:
            self.articles = json.load(f)

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        retrieved_articles = []
        determined_tags = self.tag_determiner.determine_tags(query, self.tags)
        for article in self.articles:
            article_tags = article["tags"]
            if set(article_tags) & set(determined_tags):
                retrieved_articles.append(Document(page_content=article["article"]))
        return retrieved_articles


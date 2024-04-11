from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

class HardcodedRetriever(BaseRetriever):
    documents: List[Document] = PrivateAttr(True)
    def __init__(self, articles, **kwargs: Any):
        super().__init__(**kwargs)
        self.documents = [Document(page_content="".join(article)) for article in articles]

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.documents
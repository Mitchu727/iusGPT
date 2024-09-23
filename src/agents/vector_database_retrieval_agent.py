import json

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from src.agents.retrieval_agent import RetrievalAgent
from langchain_community.vectorstores import Chroma
import src.secret import OPEN_API_KEY
from src.utils.utils import get_project_root
import os

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

class VectorDatabaseRetrievalAgent(RetrievalAgent):
    def __init__(self):
        model_name = "sdadas/mmlw-roberta-base"
        embedding_function = SentenceTransformerEmbeddings(model_name=model_name)
        docs = load_articles_as_documents()
        # db = Chroma.from_documents(docs, embedding_function, persist_directory=persist_directory)
        db = Chroma.from_documents(docs, embedding_function)
        print("There are", db._collection.count(), "documents in the collection")
        retriever = db.as_retriever(search_kwargs={"k": 20})
        retriever_prompt_template = """Here is the question:
        {question}
        And some articles that can be helpful to answer it:

        <context>
        {context}
        </context>

        Answer the given question on the base of the articles. In the answer refer to proper article.
        """
        retriever_prompt = ChatPromptTemplate.from_template(retriever_prompt_template)
        model = ChatOpenAI()

        self.retriever_chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | retriever_prompt
                | model
                | StrOutputParser()
        )

    def answer(self, question):
        return self.retriever_chain.invoke(question)

def load_articles_as_documents():
    path = get_project_root() / "documents" / "civilCodeSplitted" / "kodeks.json"
    with open(path, "r") as f:
        codex = json.load(f)
    documents = []
    for chapter in codex:
        for article in chapter["articles"]:
            document = Document(page_content=article)
            documents.append(document)
    return documents

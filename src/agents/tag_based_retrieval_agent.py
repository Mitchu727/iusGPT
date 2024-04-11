from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.agents.retrieval_agent import RetrievalAgent
from src.tag_based_retriever import TagBasedRetriever
import os
from src.secrets import OPEN_API_KEY

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class TagBasedRetrievalAgent(RetrievalAgent):

    def __init__(self):
        retriever = TagBasedRetriever()
        retriever_prompt_template = """Given the following question:
        {question}
        And related articles:

        <context>
        {context}
        </context>

        Answer the question based on the articles provided articles. Answer in polish. In the answer refer to the corresponding article.
        """

        retriever_prompt = ChatPromptTemplate.from_template(retriever_prompt_template)
        model = ChatOpenAI(model_name="gpt-3.5-turbo")

        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        self.retriever_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | retriever_prompt
                | model
                | StrOutputParser()
        )

    def answer(self, question):
        return self.retriever_chain.invoke(question)
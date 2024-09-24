from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.agents.retrieval_agent import RetrievalAgent
import src.secrets import OPEN_API_KEY
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class ChatGPT4AnsweringAgent(RetrievalAgent):
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class expert in polish civil law. Assume that all the questions regard polish civil law."
                       "In your responses refer to proper regulations."),
            ("user", "{question}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def answer(self, question):
        return self.chain.invoke({"question":question})
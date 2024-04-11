from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from src.secrets import OPEN_API_KEY


class Tagger(ABC):
    @abstractmethod
    def tag_text(self, article: str) -> list[str]:
        pass


class DummyTagger(Tagger):
    def tag_text(self, article: str) -> list[str]:
        return ["Małżeństwo"]


class ChatGPT35Tagger(Tagger):
    def __init__(self):
        self.chat = ChatOpenAI(model="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY)
        self.system_message = SystemMessage(content="You're an expert in polish civil law. Your job is to tag articles that you get with "
                                                    "the terms or ideas they are related to it. Response in polish. Do not use large letters and dots"
                                                    "In the response write only the tags separated with commas")
    def tag_text(self, article: str) -> list[str]:
        human_message = HumanMessage(content=article)
        messages = [
            human_message,
            self.system_message
        ]
        response = self.chat.invoke(messages)
        return response.content.split(", ")
from abc import ABC, abstractmethod

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
import os
import src.secret import OPEN_API_KEY
import json

class Tagger(ABC):
    @abstractmethod
    def tag_text(self, article: str) -> list[str]:
        pass


class DummyTagger(Tagger):
    def tag_text(self, article: str) -> list[str]:
        return ["Małżeństwo"]


def parse_response_into_tags(response: BaseMessage) -> list[str]:
    parsed_response = response.content.split(",")
    tags = [tag.lower().strip() for tag in parsed_response]
    if "." in tags[-1]:
        tags[-1] = tags[-1][:-1]
    return tags


class ChatGPT35Tagger(Tagger):
    def __init__(self):
        self.chat = ChatOpenAI(model="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY)
        self.system_message = SystemMessage(content="You're an expert in polish civil law. You will receive the articles from polish civil code."
                                                    "Your job is to tag them with terms, concepts and ideas they are related to."
                                                    "Try to not be too detailed"
                                                    "Every article should be tagged with maximum 5 tags"
                                                    "Response in polish. Do not use large letters and dots. Avoid making typos."
                                                    "In the response write only the tags separated with commas")

        self.tags = []

    def tag_text(self, article: str) -> list[str]:
        human_message = HumanMessage(content=article)
        messages = [
            self.system_message,
            human_message,
        ]
        response = self.chat.invoke(messages)
        tags = parse_response_into_tags(response)
        print(tags)
        self.update_tags(tags)
        return tags

    def update_tags(self, tags: list[str]):
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)

    def get_tags(self) -> list[str]:
        return self.tags

    def get_tags_as_string(self) -> str:
        return ",".join(self.tags)

    def save_tags(self):
        output_path = "../../../documents/tags.json"
        with open(output_path, "w") as f:
            json.dump(self.tags, f)

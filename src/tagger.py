from abc import ABC, abstractmethod

from langchain_core.prompts import PromptTemplate
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
        self.system_message = SystemMessage(content="You're an expert in polish civil law. You will receive the articles from polish civil code."
                                                    "Your job is to tag them with terms, concepts and ideas they are related to. Possible tags can be provided with a question, "
                                                    "but you can also come up new tags. If there are typos in article fix them."
                                                    "Response in polish. Do not use large letters and dots"
                                                    "In the response write only the tags separated with commas")
        self.tags = []
        self.prompt_template = PromptTemplate.from_template(
            "Article: {article}"
            "Tags: {tags}"
        )

    def tag_text(self, article: str) -> list[str]:
        prompt = self.prompt_template.invoke({"article": article, "tags": self.get_tags_as_string()}).to_string()
        human_message = HumanMessage(content=prompt)
        messages = [
            human_message,
            self.system_message
        ]
        response = self.chat.invoke(messages)
        tags = self.parse_response(response)
        print(tags)
        self.update_tags(tags)
        return tags

    def update_tags(self, tags: list[str]):
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)

    def parse_response(self, response: str) -> list[str]:
        parsed_response = response.content.split(", ")
        if "." in parsed_response[-1]:
            parsed_response[-1] = parsed_response[-1][:-1]
        return parsed_response

    def get_tags(self) -> list[str]:
        return self.tags

    def get_tags_as_string(self) -> str:
        return ",".join(self.tags)

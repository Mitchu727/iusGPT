from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.secrets import OPEN_API_KEY


class TagDeterminer:
        def __init__(self):
            self.chat = ChatOpenAI(model="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY)
            self.system_message = SystemMessage(
                content="You're an expert in polish civil law. Your will get a question and a list of tags."
                        "Your job is to decide which tags are related to the question."
                        "In the response write only the tags separated with commas")
            self.prompt_template = PromptTemplate.from_template(
                "Question: {question}"
                "Tags: {tags}"
            )


        def determine_tags(self, question: str, tags: list[str]) -> list[str]:
            tags_joined = "\n".join(tags)
            prompt = self.prompt_template.invoke({"question": question, "tags": tags_joined}).to_string()
            human_message = HumanMessage(content=prompt)
            messages = [
                self.system_message,
                human_message
            ]
            response = self.chat.invoke(messages)
            return response.content.split(", ")

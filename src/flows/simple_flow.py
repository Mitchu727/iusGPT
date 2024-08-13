from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.flows.flow_interface import FlowInterface
from src.secrets import OPEN_API_KEY
import os

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class SimpleFlow(FlowInterface):
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{formatted_question}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser


    def answer_evaluation_question(self, question_dict):
        formatted_question = self.format_question(question_dict)
        return self.chain.invoke({"formatted_question": formatted_question})


    def get_flow_name(self):
        return f"simple_{self.model}_{self.temperature}"

    def get_flow_parameters(self):
        return {
            'model': self.model,
            'temperature': self.temperature,
            'system_prompt': self.system_prompt,
            'evaluation_prompt_template': self.evaluation_prompt_template
        }
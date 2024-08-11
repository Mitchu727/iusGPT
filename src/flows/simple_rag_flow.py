from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.secrets import OPEN_API_KEY
import os


os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class SimpleRagFlow:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant specializing in Polish civil law. You will receive questions from 
            an exam, each consisting of a question or an incomplete sentence followed by three possible answers labeled 
            a, b, and c. 

            Your task is to:
            1. Choose the correct answer.
            2. Provide a detailed explanation for your choice.
            3. Refer to the relevant article(s) in the Polish Civil Code.

            Please ensure your responses are precise and informative. Respond in polish"""),
            ("user", "{formatted_question}")
        ])
        self.human_prompt_template = """
            Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}

            Please choose the correct answer (a, b, or c), provide an explanation, and refer to the relevant article(s) 
            in the Polish Civil Code."""
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def format_question(self, question_dict):
        return self.human_prompt_template.format(
            index=question_dict["index"],
            question=question_dict["question"],
            answer_a=question_dict["a"],
            answer_b=question_dict["b"],
            answer_c=question_dict["c"]
        )

    def answer_evaluation_question(self, question_dict):
        formatted_question = self.format_question(question_dict)
        return self.chain.invoke({"formatted_question": formatted_question})

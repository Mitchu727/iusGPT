from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.utils.utils import format_question


class AnsweringAgent:
    system_prompt = """
    You are a helpful assistant specializing in Polish civil law. You will receive questions from 
    an exam, each consisting of a question or an incomplete sentence followed by three possible answers labeled 
    a, b, and c. 

    Your task is to:
    1. Choose the correct answer.
    2. Provide a detailed explanation for your choice.
    3. Refer to the relevant article(s) in the Polish Civil Code.

    Please ensure your responses are precise and informative. Respond in polish
    In context you will receive the list of articles that might help you.
    """

    user_prompt_template = """
    {formatted_question}

    Context:
    {retrieved_articles} 
    """

    def __init__(self, model="gpt-4o-mini", temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{question_with_context}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def answer_evaluation_question(self, question_dict, retrieved_articles):
        question_with_context = self.user_prompt_template.format(formatted_question=format_question(question_dict),
                                                                 retrieved_articles=retrieved_articles)
        return self.chain.invoke({"question_with_context": question_with_context})

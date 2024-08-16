from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.utils.utils import get_project_root, format_question

dir_path = get_project_root() / "src" / "flows" / "concept_flow"


class ChapterSelector:
    system_prompt = """
    Role: You are an expert assistant specializing in Polish civil law. Your task is to analyze exam questions related to Polish civil law, where each question consists of a query or an incomplete sentence followed by three possible answers labeled "a," "b," and "c."

    Task: Based on the provided descriptions of the chapters of the Polish Civil Code, determine which chapter would be the most appropriate to consult in order to answer each question.

    Instructions:

    Carefully consider the nature of each question and the descriptions of the chapters provided.

    Your response should only include one of the following chapter titles:
        KSIĘGA PIERWSZA CZĘŚĆ OGÓLNA
        KSIĘGA DRUGA WŁASNOŚĆ I INNE PRAWA RZECZOWE
        KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_OGÓLNA
        KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_PIERWSZA
        KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_DRUGA
        KSIĘGA CZWARTA SPADKI

    Note: Provide only the chapter title as your answer, based on your analysis.

    Following chapter descriptions may help you:
    {chapters_annotated}
"""

    def __init__(self, model="gpt-4o-mini", temperature=0):
        self.model = model
        self.temperature = temperature
        with open(dir_path / "chapters_annotated.txt", "r") as f:
            chapters_annotated = f.read()

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt.format(chapters_annotated=chapters_annotated)),
            ("user", "{formatted_question}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def select_chapter(self, question_dict):
        return self.chain.invoke({"formatted_question": format_question(question_dict)})


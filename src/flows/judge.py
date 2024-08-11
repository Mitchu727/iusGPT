from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.secrets import OPEN_API_KEY
import os

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class Judge:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an assistant designed to evaluate answers from a Polish Civil Code exam. The exam 
            includes questions or incomplete sentences followed by three possible answers labeled 'a', 'b', and 'c'.

            Students must choose the correct answer and refer to the appropriate Civil Code article. You will be 
            provided with the question, the student's answer, the correct answer, and the correct article reference.

            Your response should be in JSON format and include two parts:
            - answer_is_correct: A boolean indicating whether the student chose the correct answer.
            - article_is_correct: A boolean indicating whether the student referred to the correct article. 
            If the student referred to more articles than needed but included the correct one, return true.
            """),
            ("user", "{formatted_question}")
        ])
        self.human_prompt_template = """
            Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}

            Student answer: {evaluated_answer} 
            Correct answer: {correct_answer}
            Proper article: {article}
            """
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser

    def format_question(self, question_dict, answer_dict, evaluated_answer):
        return self.human_prompt_template.format(
            index=question_dict["index"],
            question=question_dict["question"],
            answer_a=question_dict["a"],
            answer_b=question_dict["b"],
            answer_c=question_dict["c"],
            evaluated_answer=evaluated_answer,
            correct_answer=answer_dict["answer"],
            article=answer_dict["context"]
        )

    def assess_evaluation_question(self, question_dict, answer_dict, evaluated_answer):
        formatted_question = self.format_question(question_dict, answer_dict, evaluated_answer)
        return self.chain.invoke({"formatted_question": formatted_question})

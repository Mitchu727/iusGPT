from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import src.secrets
import os


class Judge:
    system_prompt = """You are an assistant designed to evaluate answers from a Polish Law exam. The exam consists of questions or incomplete sentences, each followed by three possible answers labeled 'a', 'b', and 'c'.
            
            Students are required to:
            
                Choose the correct answer.
                Refer to the appropriate law article(s) that support their chosen answer.
            
            For each student submission, you will be provided with:
            
                The question or incomplete sentence.
                The student's chosen answer.
            
            Your task is to extract the letter of student answer, and the articles student referred to (only the number without the paragraph sign) and provide a JSON output with two key-value pairs:
            
                chosen_answer: A one letter response (a, b, c) that represents the students answer.
                referred_articles: A list of integers that contain the ids of the referred articles.
            
            Your response should be in strict JSON format, starting and ending with curly braces.
            """

    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{formatted_question}")
        ])
        self.human_prompt_template = """
            Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}

            Student answer: {evaluated_answer} 
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

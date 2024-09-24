from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import src.secrets
import os


class Judge:
    system_prompt = """You are an assistant designed to evaluate answers from a Polish Civil Code exam. The exam consists of questions or incomplete sentences, each followed by three possible answers labeled 'a', 'b', and 'c'.
            
            Students are required to:
            
                Choose the correct answer.
                Refer to the appropriate Civil Code article(s) that support their chosen answer.
            
            For each student submission, you will be provided with:
            
                The question or incomplete sentence.
                The student's chosen answer.
                The correct answer.
                The correct Civil Code article reference(s).
            
            Your task is to evaluate the student's response and provide a JSON output with two key-value pairs:
            
                answer_is_correct: A boolean (true or false) indicating whether the student's chosen answer is correct.
                article_is_correct: A boolean (true or false) indicating whether the student correctly referred to the appropriate Civil Code article(s).
                    If the student references more articles than necessary but includes the correct one, return true.
                    If the student fails to reference any article, return false.
            
            Important: Ensure that your evaluation is precise. For example, if the student's chosen answer is incorrect but matches the article they referenced, answer_is_correct should still be false, even if the article they referred to is relevant to their incorrect answer.
            
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

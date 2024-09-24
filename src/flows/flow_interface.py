from abc import ABC, abstractmethod
import src.secrets


class FlowInterface(ABC):
    system_prompt = """You are a helpful assistant specializing in Polish civil law. You will receive questions from 
            an exam, each consisting of a question or an incomplete sentence followed by three possible answers labeled 
            a, b, and c. 

            Your task is to:
            1. Choose the correct answer.
            2. Provide a detailed explanation for your choice.
            3. Refer to the relevant article(s) in the Polish Civil Code.

            Please ensure your responses are precise and informative. Respond in polish."""

    evaluation_prompt_template = """
                Question: {question}

                a) {answer_a}
                b) {answer_b}
                c) {answer_c}

                Please choose the correct answer (a, b, or c), provide an explanation, and refer to the relevant article(s) 
                in the Polish Civil Code."""

    def format_question(self, question_dict):
        return self.evaluation_prompt_template.format(
            index=question_dict["index"],
            question=question_dict["question"],
            answer_a=question_dict["a"],
            answer_b=question_dict["b"],
            answer_c=question_dict["c"]
        )

    @abstractmethod
    def answer_evaluation_question(self, question_dict):
        pass

    @abstractmethod
    def get_flow_name(self):
        pass

    @abstractmethod
    def get_flow_parameters(self):
        pass

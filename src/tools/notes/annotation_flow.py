import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import src.secrets
from src.flows.flow_interface import FlowInterface
from src.utils.utils import format_question, get_project_root, format_answer, extract_id_from_article_content, \
    convert_string_to_list

DEFAULT_MODEL = "gpt-4o-mini"
dir_path = get_project_root() / "src" / "tools" / "notes"


class ChapterSelector:
    system_prompt =  """
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

    def __init__(self, model=DEFAULT_MODEL, temperature=0):
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


class ArticleSelector:
    system_prompt = """
    You will be provided with an exam question and relevant notes on articles from the Polish Civil Code. 
    The exam question may be either a direct question or an incomplete sentence, accompanied by three potential answers labeled a, b, and c. 
    Your task is to analyze the question and return a list of specific Civil Code articles that are most relevant and useful in selecting the correct answer. 
    You can choose up to 20 articles. It is better to select more than less. If the needed article won't be selected this would lead to system failure.
    When redundant articles are selected this won't have large consequences.
    If you know any Polish Civil Code article that will be helpful you can add it to list.\
    Respond in polish
    Return the list of articles as their numbers in list in format: [<number>, <number>].
    For example: [13, 12, 15]
    """
    user_prompt_templae = """
    Notes on articles from the Civil Code:
    {list_of_articles_list}
    
    Question:
    {question_dict}
    """

    def __init__(self, model=DEFAULT_MODEL, temperature=0):
        self.model = model
        self.temperature = temperature

        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", "{formatted_question}")
        ])
        output_parser = StrOutputParser()
        self.chain = prompt | llm | output_parser


    def get_selected_articles(self, question_dict, annotated_articles):
        formatted_question = self.user_prompt_templae.format(list_of_articles_list=annotated_articles, question_dict=format_question(question_dict))
        return self.chain.invoke({"formatted_question": formatted_question})


def load_articles_with_ids(article_ids):
    civil_articles_path = get_project_root() / "documents" / "legal_acts" / "civil_code" / "source.json"
    articles_to_retrieve = []
    with open(civil_articles_path, "r") as f:
        articles = json.load(f)
    for article in articles:
        content = article["content"]
        article_id = extract_id_from_article_content(content).replace("Art. ", "").replace(".", "")
        for index in article_ids:
            if index == article_id:
                articles_to_retrieve.append(content)
    return articles_to_retrieve



# class NotesFlow():
#     def __init__(self):
#         pass
#
#     def answer_evaluation_question(self, question_dict):
#         return "sth"


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
        question_with_context = self.user_prompt_template.format(formatted_question=format_question(question_dict), retrieved_articles=retrieved_articles)
        return self.chain.invoke({"question_with_context": question_with_context})

class AnnotationFlow(FlowInterface):
    def __init__(
            self,
            chapter_selector_model="gpt-3.5-turbo-0125",
            article_selector_model="gpt-3.5-turbo-0125",
            answering_agent_model="gpt-3.5-turbo-0125",
            chapter_selector_temperature=0,
            article_selector_temperature=0,
            answering_agent_temperature=0,
    ):
        self.chapter_selector_model = chapter_selector_model
        self.article_selector_model = article_selector_model
        self.answering_agent_model = answering_agent_model
        self.chapter_selector_temperature = chapter_selector_temperature
        self.article_selector_temperature = article_selector_temperature
        self.answering_agent_temperature = answering_agent_temperature
        self.chapter_selector = ChapterSelector(chapter_selector_model, chapter_selector_temperature)
        self.article_selector = ArticleSelector(article_selector_model, article_selector_temperature)
        self.answering_agent = AnsweringAgent(answering_agent_model, answering_agent_temperature)

    def answer_evaluation_question(self, question_dict):
        selected_chapter = self.chapter_selector.select_chapter(question_dict)
        annotated_articles = self.get_chapter_articles(selected_chapter)
        selected_articles = self.article_selector.get_selected_articles(question_dict, annotated_articles)
        selected_articles_list = self.extract_articles_list(selected_articles)
        retrieved_articles = "\n".join(load_articles_with_ids(selected_articles_list))
        final_answer = self.answering_agent.answer_evaluation_question(question_dict, retrieved_articles)
        return final_answer

    @staticmethod
    def get_chapter_articles(selected_chapter):
        if selected_chapter == "KSIĘGA PIERWSZA CZĘŚĆ OGÓLNA":
            chapter_file_name = "chapter_1.txt"
        elif selected_chapter == "KSIĘGA DRUGA WŁASNOŚĆ I INNE PRAWA RZECZOWE":
            chapter_file_name = "chapter_2.txt"
        elif selected_chapter == "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_OGÓLNA":
            chapter_file_name = "chapter_3.txt"
        elif selected_chapter == "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_PIERWSZA":
            chapter_file_name = "chapter_3_2.txt"
        elif selected_chapter == "KSIĘGA TRZECIA ZOBOWIĄZANIA_CZĘŚĆ_SZCZEGÓŁOWA_CZĘŚĆ_DRUGA":
            chapter_file_name = "chapter_3_2_2.txt"
        elif selected_chapter == "KSIĘGA CZWARTA SPADKI":
            chapter_file_name = "chapter_4.txt"
        else:
            chapter_file_name = "chapter_1.txt"
        with open(dir_path/ chapter_file_name, "r") as f:
            text = f.read()
        return text

    @staticmethod
    def extract_articles_list(response):
        result = re.search("\[.*]", response)
        try:
            return convert_string_to_list(result.group())
        except:
            return []


    def get_flow_name(self):
        return "annotation_flow"

    def get_flow_parameters(self):
        return {
            "chapter_selector_model" : self.chapter_selector_model,
            "article_selector_model" : self.article_selector_model,
            "answering_agent_model" : self.answering_agent_model,
            "chapter_selector_temperature" : self.chapter_selector_temperature,
            "article_selector_temperature" : self.article_selector_temperature,
            "answering_agent_temperature" : self.answering_agent_temperature,
        }


# if __name__ == "__main__":
    # dataset_path = get_project_root() / "documents" / "evaluation" / "civil_law_exam"
    # questions_path = dataset_path / "questions.json"
    # answers_path = dataset_path / "answers.json"
    #
    # with open(questions_path, "r") as f:
    #     questions = json.load(f)
    #
    # with open(answers_path, "r") as f:
    #     answers = json.load(f)
    #
    # chapter_selector = ChapterSelector()
    # article_selector = ArticleSelector()
    # answering_agent = AnsweringAgent()
    # for i in range(10):
    #     question_dict = questions[i]
    #     answer_dict = answers[i]
    #
    #     print("==========PYTANIE==========")
    #     print(format_question(question_dict))
    #
    #     print("==========PRAWIDŁOWA ODPOWIEDŹ==========")
    #     print(format_answer(answer_dict))
    #
    #     print("==========WYBRANY ROZDZIAŁ==========")
    #     selected_chapter = chapter_selector.select_chapter(question_dict)
    #     print(selected_chapter)
    #     print("==========WYBRANE ARTYKUŁY==========")
    #     annotated_articles = AnnotationFlow.get_chapter_articles(selected_chapter)
    #     selected_articles = article_selector.get_selected_articles(question_dict, selected_chapter)  # TODO VERY STRANGE
    #     # selected_articles = article_selector.get_selected_articles(question_dict, annotated_articles)
    #     print(selected_articles)
    #     selected_articles_list = AnnotationFlow.extract_articles_list(selected_articles)
    #     retrieved_articles = "\n".join(load_articles_with_ids(selected_articles_list))
    #     final_answer = answering_agent.answer_evaluation_question(question_dict, retrieved_articles)
    #     print("==========OSTATECZNA ODPOWIEDŹ==========")
    #     print(final_answer)
    #     print("\n\n")

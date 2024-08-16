import json
import re

from src.flows.concept_flow.answering_agent import AnsweringAgent
from src.flows.concept_flow.article_selector import ArticleSelector
from src.flows.flow_interface import FlowInterface
from src.flows.concept_flow.chapter_selector import ChapterSelector
from src.utils.utils import format_question, get_project_root, extract_id_from_article_content, \
    convert_string_to_list

DEFAULT_MODEL = "gpt-4o-mini"
dir_path = get_project_root() / "src" / "flows" / "concept_flow"


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


class ConceptFlow(FlowInterface):
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
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.utils.utils import format_question

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
    user_prompt_template = """
    Notes on articles from the Civil Code:
    {list_of_articles_list}

    Question:
    {question_dict}
    """

    def __init__(self, model="gpt-4o-mini", temperature=0):
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
        formatted_question = self.user_prompt_template.format(list_of_articles_list=annotated_articles,
                                                             question_dict=format_question(question_dict))
        return self.chain.invoke({"formatted_question": formatted_question})

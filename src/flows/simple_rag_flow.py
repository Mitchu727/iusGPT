from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from src.secrets import OPEN_API_KEY
import os

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY


class SimpleRagFlow:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0):
        docs = load_articles_as_documents()
        retriever = create_chroma_retriever(docs, 10)
        retriever_tool = create_retriever_tool(
            retriever,
            "civil_code",
            "Search for information in polish civil code.",
        )
        tools = [retriever_tool]
        llm = ChatOpenAI(model=model, temperature=temperature)

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=[],
                    template="""You are a helpful assistant specializing in Polish civil law. You will receive questions from 
                    an exam, each consisting of a question or an incomplete sentence followed by three possible answers labeled 
                    a, b, and c. 

                    Your task is to:
                    1. Choose the correct answer.
                    2. Provide a detailed explanation for your choice.
                    3. Refer to the relevant article(s) in the Polish Civil Code.

                    Please ensure your responses are precise and informative. Respond in polish"""
                )
            ),
            MessagesPlaceholder(variable_name='chat_history', optional=True),
            HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ])
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        self.human_prompt_template = """
            Question: {question}

            a) {answer_a}
            b) {answer_b}
            c) {answer_c}

            Please choose the correct answer (a, b, or c), provide an explanation, and refer to the relevant article(s) 
            in the Polish Civil Code."""

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
        return self.agent_executor.invoke({"input": formatted_question})["output"]

import json
import string
from typing import TypedDict, Annotated, Sequence, Literal, List

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from src.flows.flow_interface import FlowInterface
from langgraph.graph import StateGraph, START, END, add_messages

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.tools.retriever.extended_retriever import ExtendedRetriever
from src.tools.retriever.prefixed_retriever import PrefixedRetriever
from src.utils.utils import get_example_question, get_hard_example_question, get_legal_act_json_path, \
    get_hard_retrieval_question, get_project_root
import src.secrets
import functools


class State(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    question: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    regulations: List[Document]


class MultiAgentFlowAdvancedRag(FlowInterface):
    supported_codes = ['civil_code']

    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0, k=10):
        self.model = model
        self.temperature = temperature
        self.k = k
        self.workflow = self.create_workflow_graph(model, temperature, k)

    @staticmethod
    def create_retriever_tool(k, code):
        print(f"Creating retriever tool for {code}")
        docs = load_articles_as_documents(get_legal_act_json_path(code))
        base_retriever = create_chroma_retriever(docs, code, k, False)
        retriever = PrefixedRetriever(retriever=base_retriever)
        # prefixed_retriever = PrefixedRetriever(retriever=base_retriever)
        # retriever = ExtendedRetriever(retriever=prefixed_retriever, range=2, docs=docs)
        retriever_tool = create_retriever_tool(
            retriever,
            code,
            f"Search for information in polish {code.replace("_", " ")}.",
        )
        return retriever
        # return retriever_tool

    def create_retrieval_agent(self, model, temperature):
        prompt = """
        You are an intelligent retriever agent tasked with retrieving relevant regulations from the Polish law regulations. 
        The regulations are stored in a vector database. Upon receiving a user query, your responsibilities are as follows:

        Provide the answer in 5 lines. Here is what they should contain:
        Line 1: Do you know what polish regulation may be answering this question? Write the content of such regulation.
        Line 2: Imagine a regulation that answers the following questions. Write the content of imagined regulation.
        Line 3: Extract the all relevant concepts from the question and provide a list separated by spaces like: incapacitation adult mental illness
        Line 4: Formulate a simple question about the concepts from the question.
        Line 5: Formulate detailed question that covers all concepts from the question.
        
        Pay attention to cover each part of the question in the upper lines. Do not include Line word in the answer.
        
        Respond in Polish.
        """
        llm = ChatOpenAI(temperature=temperature, model=model)
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return prompt | llm

    def create_answering_agent(self, model, temperature):
        prompt = self.system_prompt + "You will also receive some regulations that will help you."
        human_template = """{question}
        
        Here are some regulations that can help you.
        {regulations}
        """
        llm = ChatOpenAI(temperature=temperature, model=model)
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=prompt),
                HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['question', 'regulations'], template=human_template)),
            ]
        )
        return prompt | llm

    def create_workflow_graph(self, model, temperature, k):
        workflow = StateGraph(State)

        workflow.add_edge(START, "retrieval_agent")

        def general_retrieval_agent_node(state: State, retriever) -> State:
            prompts = self.create_retrieval_agent(model, temperature).invoke({"messages": [state["question"]]})
            documents = []
            for prompt in prompts.content.split('\n'):
                if prompt.strip() != "":
                    print(prompt)
                    documents.extend(retriever.invoke(prompt))
            return {
                "regulations": documents
            }

        def answering_agent_node(state: State) -> State:
            print("answering...")
            regulations_string = [regulation.page_content for regulation in state["regulations"]]
            answer = self.create_answering_agent(model, temperature).invoke(
                {
                    "question": state["question"],
                    "regulations": "\n".join(regulations_string)
                }
            )
            return {
                "messages": [answer]
            }

        code = "civil_code"
        retriever = self.create_retriever_tool(k, code)
        retrieval_agent = functools.partial(general_retrieval_agent_node, retriever=retriever)
        workflow.add_node("retrieval_agent", retrieval_agent)
        # workflow.add_edge("retrieval_agent", END)

        workflow.add_node(f"answering_agent", answering_agent_node)
        workflow.add_edge("retrieval_agent", "answering_agent")
        workflow.add_edge("answering_agent", END)
        return workflow

    def save_graph_image(self, path="graph.png"):
        graph = self.workflow.compile()
        image = graph.get_graph(xray=True).draw_mermaid_png()

        with open(path, "wb") as png:
            png.write(image)

    def answer_evaluation_question(self, question_dict):
        graph = self.workflow.compile()
        formatted_question = self.format_question(question_dict)
        inputs = {
            "question": formatted_question,
            "messages": [
                HumanMessage(content=formatted_question)
            ]
        }
        result = graph.invoke(inputs)
        for regulation in result["regulations"]:
            print(regulation.page_content)
        ChatPromptTemplate.from_messages(result["messages"]).pretty_print()
        return result["messages"][-1].content

    def get_flow_name(self):
        return f"multi_agent_advanced_rag{self.model}_{self.temperature}"

    def get_flow_parameters(self):
        return {
            'model': self.model,
            'temperature': self.temperature,
            'k': self.k,
            'system_prompt': self.system_prompt,
            'evaluation_prompt_template': self.evaluation_prompt_template,
            'vectorstore': 'chroma'
        }


def load_questions_for_codes(code_list):
    questions = []
    answers = []
    for code in code_list:
        dataset_path = get_project_root() / "documents" / "evaluation" / "extracted" / code
        questions_path = dataset_path / "questions.json"
        answers_path = dataset_path / "answers.json"
        with open(questions_path, "r") as f:
            code_questions = json.load(f)
        questions.extend(code_questions)
        with open(answers_path, "r") as f:
            code_answers = json.load(f)
        answers.extend(code_answers)
    return questions, answers



if __name__ == '__main__':
    # flow = MultiAgentFlow("gpt-3.5-turbo-0125", 0, 30)
    flow = MultiAgentFlowAdvancedRag("gpt-4o-mini", 0, 20)
    flow.save_graph_image()
    # question = get_example_question()
    question = get_hard_retrieval_question()
    questions, answers = load_questions_for_codes(["civil_code"])
    for i in [29, 126, 132]:
        print("============QUESTION==============")
        print(questions[i])
        print(flow.answer_evaluation_question(questions[i]))

        print("=============GOOD ANSWER========")
        print(answers[i])

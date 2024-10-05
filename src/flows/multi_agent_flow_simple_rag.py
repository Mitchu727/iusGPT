import string
from typing import TypedDict, Annotated, Sequence, Literal

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from src.flows.flow_interface import FlowInterface
from langgraph.graph import StateGraph, START, END, add_messages

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.tools.retriever.prefixed_retriever import PrefixedRetriever
from src.utils.utils import get_example_question, get_hard_example_question, get_legal_act_json_path
import src.secrets
import functools


class State(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


class MultiAgentFlowSimpleRag(FlowInterface):
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
        retriever_tool = create_retriever_tool(
            retriever,
            code,
            f"Search for information in polish {code.replace("_", " ")}.",
        )
        return retriever_tool

    def create_code_agent(self, model, temperature, tools):
        llm = ChatOpenAI(temperature=temperature, model=model)
        llm_with_tools = llm.bind_tools(tools)
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        return prompt | llm_with_tools

    def create_workflow_graph(self, model, temperature, k):

        workflow = StateGraph(State)

        workflow.add_edge(START, "civil_code_agent")


        def generic_code_agent_node(state: State, retriever_tool) -> State:
            return {
                "messages": [self.create_code_agent(model, temperature, [retriever_tool]).invoke(state['messages'])]
            }

        code = "civil_code"
        retriever_tool = self.create_retriever_tool(k, code)
        code_agent_node = functools.partial(generic_code_agent_node, retriever_tool=retriever_tool)
        workflow.add_node(f"{code}_agent", code_agent_node)
        civil_code_retrieve = ToolNode([retriever_tool])
        workflow.add_node(f"{code}_retrieve", civil_code_retrieve)
        workflow.add_edge(f"{code}_retrieve", f"{code}_agent")
        workflow.add_conditional_edges(
            f"{code}_agent",
            tools_condition,
            {
                "tools": f"{code}_retrieve",
                END: END,
            },
        )
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
            "messages": [
                HumanMessage(content=formatted_question)
            ]
        }
        result = graph.invoke(inputs)
        ChatPromptTemplate.from_messages(result["messages"]).pretty_print()
        return result["messages"][-1].content

    def get_flow_name(self):
        return f"multi_agent_simple_rag{self.model}_{self.temperature}"

    def get_flow_parameters(self):
        return {
            'model': self.model,
            'temperature': self.temperature,
            'k': self.k,
            'system_prompt': self.system_prompt,
            'evaluation_prompt_template': self.evaluation_prompt_template,
            'vectorstore': 'chroma'
        }


if __name__ == '__main__':
    # flow = MultiAgentFlow("gpt-3.5-turbo-0125", 0, 30)
    flow = MultiAgentFlow("gpt-4o-mini", 0, 30)
    # question = get_example_question()
    question = get_hard_example_question()

    print("============FINAL ANSWER==============")
    print(flow.answer_evaluation_question(question))
    flow.save_graph_image()

    print("=============GOOD ANSWER========")
    print("A")

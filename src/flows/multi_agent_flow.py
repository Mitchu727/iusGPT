from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

from src.flows.flow_interface import FlowInterface
from langgraph.graph import StateGraph, START, END, add_messages

from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.tools.retriever.prefixed_retriever import PrefixedRetriever
from src.utils.utils import get_example_question
import src.secret



class State(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


class MultiAgentFlow(FlowInterface):
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0, k=10):
        self.model = model
        self.temperature = temperature
        self.k = k
        self.workflow = self.create_workflow_graph(model, temperature, k)

    @staticmethod
    def create_retriever_tool(k):
        docs = load_articles_as_documents()
        base_retriever = create_chroma_retriever(docs, k)
        retriever = PrefixedRetriever(retriever=base_retriever)
        retriever_tool = create_retriever_tool(
            retriever,
            "civil_code",
            "Search for information in polish civil code.",
        )
        return retriever_tool

    def create_base_agent(self, model, temperature, tools):
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
        retriever_tool = self.create_retriever_tool(k)

        def base_agent_node(state: State) -> State:
            return {
                "messages": [self.create_base_agent(model, temperature, [retriever_tool]).invoke(state['messages'])]}

        workflow.add_node("base_agent", base_agent_node)
        workflow.add_edge(START, "base_agent")

        retrieve = ToolNode([retriever_tool])
        workflow.add_node("retrieve", retrieve)
        workflow.add_edge("retrieve", "base_agent")

        workflow.add_conditional_edges(
            "base_agent",
            tools_condition,
            {
                "tools": "retrieve",
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
        return f"multi_agent_{self.model}_{self.temperature}"

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
    flow = MultiAgentFlow("gpt-3.5-turbo-0125", 0, 30)
    question = get_example_question()

    print("============FINAL ANSWER==============")
    print(flow.answer_evaluation_question(question))
    flow.save_graph_image()
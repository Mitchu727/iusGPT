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
from src.utils.utils import get_example_question, get_hard_example_question
import src.secrets


class State(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


class GradeAnswer(BaseModel):
    """Binary score for reasoning in generated answer."""

    binary_score: str = Field(
        description="Answer is reasonable and contains no reasoning errors, 'yes' or 'no'"
    )


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

    def create_feedback_agent(self, model, temperature):
        llm = ChatOpenAI(temperature=temperature, model=model)
        feedback_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="""
                    You are tasked with reviewing the responses of a legal assistant. Your role is to assess the 
                    quality of their legal reasoning, ensuring that the response is accurate, clear, and well-argued.

                    Feedback: Assess the quality of assistant's reasoning. Think step by step.
                    Step 1: Analyze the text of the referred article.
                    Step 2: Check if the answer corresponds to the given article.
                    Step 3: If it's not, write what's wrong and what to pay attention to. 

                    Assessment: If the response requires improvement, write "IMPROVE" and specify the areas that need further attention.
                    """),
                MessagesPlaceholder(variable_name="messages")
                # HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}'))
            ]
        )
        return feedback_prompt | llm

    def create_workflow_graph(self, model, temperature, k):
        workflow = StateGraph(State)
        retriever_tool = self.create_retriever_tool(k)

        def base_agent_node(state: State) -> State:
            return {
                "messages": [self.create_base_agent(model, temperature, [retriever_tool]).invoke(state['messages'])]}

        def feedback_agent_node(state: State) -> State:
            return {
                "messages": [self.create_feedback_agent(model, temperature).invoke([state['messages'][-1]])]
            }
        #     TODO zastanowić się nad przeniesieniem tego do LLM'a

        def feedback_router(state: State) -> Literal["improve", "__end__"]:
            messages = state["messages"]
            last_message = messages[-1].content
            if "IMPROVE" in last_message:
                return "improve"
            return "__end__"

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
                END: "feedback_agent",
            },
        )

        workflow.add_node("feedback_agent", feedback_agent_node)
        workflow.add_conditional_edges(
            "feedback_agent",
            feedback_router,
            {
                "improve": "base_agent",
                "__end__": END
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
        return result["messages"][-2].content

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
    # flow = MultiAgentFlow("gpt-4o-mini", 0, 30)
    # question = get_example_question()
    question = get_hard_example_question()

    print("============FINAL ANSWER==============")
    print(flow.answer_evaluation_question(question))
    flow.save_graph_image()

    print("=============GOOD ANSWER========")
    print("A")
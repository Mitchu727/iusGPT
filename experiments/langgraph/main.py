from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END, MessageGraph
from src.secrets import OPEN_API_KEY, TAVILY_API_KEY
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

model = ChatOpenAI(temperature=0)

graph = MessageGraph()

graph.add_node("oracle", model)
graph.add_edge("oracle", END)

graph.set_entry_point("oracle")


from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def multiply(first_number: int, second_number: int):
    """Multiplies two numbers together."""
    return first_number * second_number

model = ChatOpenAI(temperature=0)
model_with_tools = model.bind_tools([multiply])

builder = MessageGraph()

builder.add_node("oracle", model_with_tools)

tool_node = ToolNode([multiply])
builder.add_node("multiply", tool_node)

builder.add_edge("multiply", END)

builder.set_entry_point("oracle")

from typing import Literal, List


def router(state: List[BaseMessage]) -> Literal["multiply", "__end__"]:
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "multiply"
    else:
        return "__end__"

builder.add_conditional_edges("oracle", router)

runnable = builder.compile()

# print(runnable.invoke(HumanMessage("What is 123 * 456?")))

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

tools = [TavilySearchResults(max_results=1)]


tool_node = ToolNode(tools)

from langchain_openai import ChatOpenAI

# We will set streaming=True so that we can stream tokens
# See the streaming section for more information on this.
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
model = model.bind_tools(tools)

from typing import TypedDict, Annotated

def add_messages(left: list, right: list):
    """Add-don't-overwrite."""
    return left + right

class AgentState(TypedDict):
    # The `add_messages` function within the annotation defines
    # *how* updates should be merged into the state.
    messages: Annotated[list, add_messages]

from typing import Literal

# Define the function that determines whether to continue or not
def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return "__end__"


# Define the function that calls the model
def call_model(state: AgentState):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


from langgraph.graph import StateGraph, END
# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", 'agent')

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="""
What is the correct answer for this question:
Uznania czynności prawnej dokonanej z pokrzywdzeniem wierzycieli za bezskuteczną nie można żądać po upływie
a) 3 lat od daty tej czynności
 b) 5 lat od daty tej czynności
 c) 10 lat od daty tej czynności
""")]}
print(app.invoke(inputs))
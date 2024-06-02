import json

import pandas as pd
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

from src.knowledge_graph.networkX.utils import create_graph
from src.utils.utils import get_project_root
from src.secrets import OPEN_API_KEY

question = "Kim jest osoba ubezwłasnowolniona?"

input_path = get_project_root() / "documents" / "knowledge_graph" / "graph.json"
G = create_graph(input_path)

SYS_PROMPT = SystemMessage(
    content= "You are assistant of lawyer and your job is to help him answer given questions with knowledge graph."
    "You will receive a question and a list of nodes in the graph and you have to decide which nodes are relevant for the question"
    "\n\n Output format: return only the relevant nodes separated by commas, do not use quotation marks"
)

USER_PROMPT_TEMPLATE = PromptTemplate.from_template("question: {question} \n\n nodes: {nodes}")
model = ChatOpenAI(model_name="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY, temperature=0)
USER_MESSAGE = USER_PROMPT_TEMPLATE.invoke({"question": question, "nodes": G.nodes}).to_string()
messages = [
    SYS_PROMPT,
    USER_MESSAGE
]

response = model.invoke(messages)
print(response.content)
for node in response.content.split(", "):
    print(node)

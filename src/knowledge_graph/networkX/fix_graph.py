import json

import pandas as pd
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

from src.knowledge_graph.networkX.utils import create_graph
from src.utils.utils import get_project_root
from src.secrets import OPEN_API_KEY

input_path = get_project_root() / "documents" / "knowledge_graph" / "graph.json"
output_path = get_project_root() / "documents" / "knowledge_graph" / "fix_nodes.json"

G = create_graph(input_path)
print(G.nodes)

SYS_PROMPT = SystemMessage(
    content= "You are a network graph maker who extracts terms and their relations from a given context. "
    "You are fixing the graph that someone else made. The graph contained the knowledge about polish civil law"
    "Thought 1: You will get a list of nodes in the graph. Some of them refer to the same term or idea but have different grammar forms (f.e. one is singular and the other is plural)"
    "Thought 2: Unify the naming convention by proposing with the new names for each of the repeated nodes \n\n"
    "Thought 3 prefer lowercase, singular form and nominatives"
    "Format your output as a list of json. Each element of the list contains old name and new name like the following: \n"
    "[\n"
    "   {\n"
    '       "old_name": "current name of the node",\n'
    '       "new_name": "new name that the node should be renamed to to make graph more consistent",\n'
    "   }, {...}\n"
    "]"
    "Answer in polish"
)

USER_PROMPT_TEMPLATE = PromptTemplate.from_template("nodes: {nodes} \n\n output: ")
# model = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPEN_API_KEY, temperature=0)
model = ChatOpenAI(model_name="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY, temperature=0)

USER_MESSAGE = USER_PROMPT_TEMPLATE.invoke({"nodes": G.nodes}).to_string()
messages = [
    SYS_PROMPT,
    USER_MESSAGE
]

response = model.invoke(messages)
print(response.content)
structured_response = json.loads(response.content)

print(structured_response)
with open(output_path, "w") as f:
    json.dump(structured_response, f)
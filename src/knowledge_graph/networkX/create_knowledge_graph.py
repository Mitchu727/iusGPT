import json

from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from src.secrets import OPEN_API_KEY
import pandas as pd
import re
from src.utils.utils import get_project_root


def extract_id_from_article(article):
    result = re.search("Art. [0-9]*.", article)
    return result.group()

input_path = get_project_root() / "documents" / "civilCodeSplitted" / "kodeks.json"
output_path = get_project_root() / "documents" / "knowledge_graph" / "graph.json"
with open(input_path, "r") as f:
    codex = json.load(f)

articles = []
for chapter in codex[:10]:
    for article in chapter["articles"]:
        articles.append(article)


SYS_PROMPT = SystemMessage(
    content= "You are a network graph maker who extracts terms and their relations from a given context. "
    "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
    "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
    "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
        "\tTerms may include object, entity, location, organization, person, \n"
        "\tcondition, acronym, documents, service, concept, etc.\n"
        "\tTerms should be as atomistic as possible\n\n"
    "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
        "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
        "\tTerms can be related to many other terms\n\n"
    "Thought 3: Find out the relation between each such related pair of terms. \n\n"
    "Format your output as a list of json. Each element of the list contains a pair of terms"
    "and the relation between them, like the follwing: \n"
    "[\n"
    "   {\n"
    '       "node_1": "A concept from extracted ontology",\n'
    '       "node_2": "A related concept from extracted ontology",\n'
    '       "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"\n'
    "   }, {...}\n"
    "]"
    "Answer in polish"
)

USER_PROMPT_TEMPLATE = PromptTemplate.from_template("context: {article} \n\n output: ")
# model = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPEN_API_KEY, temperature=0)
model = ChatOpenAI(model_name="gpt-3.5-turbo-0125", openai_api_key=OPEN_API_KEY, temperature=0)

edges = []
for article in articles:
    article_id = extract_id_from_article(article)
    article_without_index = article.replace(article_id, "")
    USER_MESSAGE = USER_PROMPT_TEMPLATE.invoke({"article": article_without_index}).to_string()
    messages = [
        SYS_PROMPT,
        USER_MESSAGE
    ]

    response = model.invoke(messages)
    structured_response = json.loads(response.content)
    for element in structured_response:
        element["id"] = extract_id_from_article(article)
    edges.extend(structured_response)
    print(structured_response)

with open(output_path, "w") as f:
    json.dump(edges, f)

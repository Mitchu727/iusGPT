import json

import pandas as pd
from src.utils.utils import get_project_root
import networkx as nx

fix_input_path = get_project_root() / "documents" / "knowledge_graph" / "fix_nodes.json"

with open(fix_input_path, "r") as f:
    fixes = json.load(f)

# def repair_node_name(node_name):
#     for record in fixes:
#         if record["old_name"] == node_name:
#             return record["new_name"].lowercase()
#     return node_name.lowercase()

def create_graph(input_path):
    df = pd.read_json(input_path)
    nodes = pd.concat([df['node_1'], df['node_2']], axis=0).unique()

    G = nx.Graph()

    ## Add nodes to the graph
    for node in nodes:
        G.add_node(
            str(node)
        )

    ## Add edges to the graph
    for index, row in df.iterrows():
        G.add_edge(
            str(row["node_1"]),
            str(row["node_2"]),
            title=row["edge"],
        )
    return G
import pandas as pd
import numpy as np
from src.knowledge_graph.networkX.utils import create_graph
from src.utils.utils import get_project_root

input_path = get_project_root() / "documents" / "knowledge_graph" / "graph.json"

G = create_graph(input_path)

from pyvis.network import Network

graph_output_directory = str(get_project_root() / "index.html")

net = Network(
    notebook=False,
    # bgcolor="#1a1a1a",
    cdn_resources="remote",
    height="900px",
    width="100%",
    select_menu=True,
    # font_color="#cccccc",
    filter_menu=False,
)

net.from_nx(G)
# net.repulsion(node_distance=150, spring_length=400)
net.force_atlas_2based(central_gravity=0.015, gravity=-31)
# net.barnes_hut(gravity=-18100, central_gravity=5.05, spring_length=380)
# net.show_buttons(filter_=["physics"])

net.show(graph_output_directory, notebook=False)

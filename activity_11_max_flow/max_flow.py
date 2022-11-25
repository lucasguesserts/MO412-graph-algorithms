import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

current_dir = os.path.abspath(os.path.dirname(__file__))
output_dir = os.path.join(os.path.abspath(os.getcwd()), "output")
os.makedirs(output_dir, exist_ok=True)
data_dir: str = os.path.join(current_dir, "data")


def read_graph(nodes_file_path: str, arcs_file_path: str) -> nx.Graph:
    # data
    node_map = dict(
        map(
            lambda x: [int(x[1]), str(x[0])],
            list(np.loadtxt(nodes_file_path, delimiter=",", dtype=str)),
        )
    )
    edge_list = np.loadtxt(arcs_file_path, delimiter=",", dtype=np.int_)
    # graph
    graph = nx.Graph()
    for node_number, node_name in node_map.items():
        graph.add_node(node_number, name=node_name)
    for u, v, c in edge_list:
        graph.add_edge(u, v, capacity=c)
    return graph


def draw_graph(digraph: nx.DiGraph) -> None:
    options = {
        "node_color": "white",
        "edgecolors": "black",
        "with_labels": True,
        "labels": dict(
            map(
                lambda node: [node[0], f"{node[0]}_{node[1]}"],
                digraph.nodes(data="name"),
            )
        ),
    }
    nx.draw_circular(digraph, **options)
    plt.savefig(os.path.join(output_dir, "graph.png"))


if __name__ == "__main__":
    nodes_file_path: str = os.path.join(data_dir, "nodes.csv")
    edges_file_path: str = os.path.join(data_dir, "links.csv")
    graph = read_graph(nodes_file_path, edges_file_path)
    draw_graph(graph)
    source_node = 6
    target_node = 3
    max_flow = nx.maximum_flow(graph, source_node, target_node)[0]
    print(max_flow)

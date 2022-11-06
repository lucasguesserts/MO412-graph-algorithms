import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

logs = False
current_dir = os.path.abspath(os.path.dirname(__file__))
output_dir = os.path.join(
    os.path.abspath(os.getcwd()),
    "output"
)
os.makedirs(output_dir, exist_ok=True)
data_dir: str = os.path.join(current_dir, "data")


def read_digraph(nodes_file_path: str, arcs_file_path: str) -> nx.DiGraph:
    # data
    node_map = dict(map(lambda x: [int(x[0]), str(x[1])], list(np.loadtxt(
        nodes_file_path,
        delimiter = ",",
        dtype = str
    ))))
    arc_list = np.loadtxt(
        arcs_file_path,
        delimiter = ",",
        dtype = np.int_
    )
    # graph
    digraph = nx.DiGraph()
    for node_number, node_name in node_map.items():
        digraph.add_node(node_number, name=node_name)
    for arc in arc_list:
        digraph.add_edge(*arc)
    # assertions
    expected_number_of_nodes = len(node_map)
    number_of_nodes = digraph.number_of_nodes()
    assert number_of_nodes == expected_number_of_nodes
    expected_number_of_edges = np.shape(arc_list)[0]
    number_of_edges = digraph.number_of_edges()
    assert number_of_edges == expected_number_of_edges
    # return
    return digraph

def draw_digraph(digraph: nx.DiGraph) -> None:
    options = {
        "node_color": "white",
        "edgecolors": "black",
        "with_labels": True,
        "arrows": True,
        # "labels": dict(map(
        #     lambda node: [node[0], f"{node[0]}_{node[1]}"],
        #     digraph.nodes(data="name")
        # )),
    }
    nx.draw_planar(digraph, **options)
    plt.savefig(os.path.join(output_dir, "graph.png"))

def set_digraph_node_color_by_strongly_connected_components(digraph: nx.DiGraph) -> nx.DiGraph:
    digraph_component_list: list[int] = list(nx.strongly_connected_components(digraph))
    node_component_dict = dict()
    for index, component in enumerate(digraph_component_list):
        for node in component:
            node_component_dict[node] = index
    nx.set_node_attributes(
        digraph,
        node_component_dict,
        "component"
    )
    if logs:
        print("digraph_component_list ", digraph_component_list)
        print("node_component_dict ", node_component_dict)
    return

def export_to_gephi(digraph: nx.DiGraph, file_path: str) -> None:
    with open(file_path, "w") as file:
        linefeed = chr(10)
        s = linefeed.join(nx.generate_gexf(digraph))
        for line in nx.generate_gexf(digraph):
            file.write(line)
    return


if __name__ == "__main__":
    nodes_file_path: str = os.path.join(data_dir, "nodes.csv")
    arcs_file_path: str = os.path.join(data_dir, "links.csv")
    gephi_file_path: str = os.path.join(output_dir, "strongly_connected_components.gexf")
    digraph = read_digraph(nodes_file_path, arcs_file_path)
    draw_digraph(digraph)
    set_digraph_node_color_by_strongly_connected_components(digraph)
    if logs:
        for node in digraph.nodes(data=True):
            print(node)
    export_to_gephi(digraph, gephi_file_path)

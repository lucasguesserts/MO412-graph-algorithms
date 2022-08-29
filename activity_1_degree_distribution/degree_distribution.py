import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

current_dir = os.path.abspath(os.path.dirname(__file__))
output_dir = os.path.join(
    os.path.abspath(os.getcwd()),
    "output"
)
os.makedirs(output_dir, exist_ok=True)


# data
edge_list = np.loadtxt(
    os.path.join(current_dir, "phonecalls.edgelist.txt"),
    delimiter = "\t",
    dtype = np.int_
)


# graph
graph = nx.DiGraph()

for edge in edge_list:
    graph.add_edge(*edge)


# minor assertions
expected_number_of_nodes = np.max(edge_list) + 1
number_of_nodes = graph.number_of_nodes()
assert number_of_nodes == expected_number_of_nodes
expected_number_of_edges = np.shape(edge_list)[0]
number_of_edges = graph.number_of_edges()
assert number_of_edges == expected_number_of_edges


df = pd.DataFrame(
    index = graph.nodes
)
df["in_degree"] = list(map( lambda x: x[1], graph.in_degree))
df["out_degree"] = list(map( lambda x: x[1], graph.out_degree))


def plot_count_column(column_name):
    count = df[column_name].value_counts()
    
    x = count.index
    y = count.values / np.sum(count.values)

    xlim = [
        1,
        10**np.ceil(np.log10(np.max(x)))
    ]

    plt.loglog(
        x,
        y,
        linestyle="",
        marker=".",
        color = 'k',
    )
    
    plt.title(f"{column_name} distribution")
    
    plt.xlim(xlim)
    plt.ylim([None, 1])
    
    plt.xlabel("k")
    plt.ylabel("p_k")
    
    plt.grid(True)

    plt.savefig(os.path.join(output_dir, f"{column_name}.png"))

    plt.close()


plot_count_column("in_degree")


plot_count_column("out_degree")


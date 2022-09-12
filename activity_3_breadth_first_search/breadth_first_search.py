import os
from collections import deque
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
initial_node = 6
node_map = dict(map(lambda x: [int(x[0]), x[1]], list(np.loadtxt(
    os.path.join(current_dir, "data/nodes.csv"),
    delimiter = ",",
    dtype = str
))))
edge_list = np.loadtxt(
    os.path.join(current_dir, "data/edges.csv"),
    delimiter = ",",
    dtype = np.int_
)


# graph
graph = nx.Graph()

for edge in edge_list:
    graph.add_edge(*edge)


# assertions
expected_number_of_nodes = len(node_map)
number_of_nodes = graph.number_of_nodes()
assert number_of_nodes == expected_number_of_nodes
# expected_number_of_edges = np.shape(edge_list)[0]
# number_of_edges = graph.number_of_edges()
# assert number_of_edges == expected_number_of_edges


# draw graph
options = {
    "node_color": "white",
    "edgecolors": "black",
    "with_labels": True,
}
nx.draw_planar(graph, **options)
plt.savefig(os.path.join(output_dir, "graph.png"))


class NodeInfo:
    def __init__(self, parent_node, distance_from_initial_node):
        self.parent = parent_node
        self.distance = distance_from_initial_node
        return


# breadth-first search
class BFS:

    def __init__ (self, graph: nx.DiGraph, initial_node):
        self.graph = graph
        self.initial_node = initial_node
        self.parent: dict[int, NodeInfo] = dict()
        self.search()
        return

    def search(self):
        queue = deque()
        self.parent[self.initial_node] = NodeInfo(-1, 0)
        queue.append(self.initial_node)
        while len(queue) > 0:
            node = queue.popleft()
            info = self.parent[node]
            for child_node in graph.neighbors(node):
                if child_node not in self.parent.keys():
                    self.parent[child_node] = NodeInfo(node, info.distance + 1)
                    queue.append(child_node)
        return

    def save(self):
        node_info = pd.DataFrame(
            list(map(
                lambda n: [node_map[n], n, self.parent[n].parent, self.parent[n].distance],
                sorted(self.parent.keys())
            )),
            columns = ["node name", "node number", "parent", "distance"]
        )
        node_info["node name"] = node_info["node name"].astype(str)
        node_info["node number"] = node_info["node number"].astype(int)
        node_info["parent"] = node_info["parent"].astype(int)
        node_info["distance"] = node_info["distance"].astype(int)
        node_info.to_csv(
            os.path.join(output_dir, "nodes.csv"),
            sep = ",",
            line_terminator = "\n",
            index = False,
            header = False
        )
        return

dfs = BFS(graph, initial_node)
dfs.save()
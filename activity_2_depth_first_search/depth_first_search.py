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
graph = nx.DiGraph()

for edge in edge_list:
    graph.add_edge(*edge)


# assertions
expected_number_of_nodes = len(node_map)
number_of_nodes = graph.number_of_nodes()
assert number_of_nodes == expected_number_of_nodes
expected_number_of_edges = np.shape(edge_list)[0]
number_of_edges = graph.number_of_edges()
assert number_of_edges == expected_number_of_edges


# draw graph
options = {
    "node_color": "white",
    "edgecolors": "black",
    "with_labels": True,
}
nx.draw_planar(graph, **options)
plt.savefig(os.path.join(output_dir, "graph.png"))


# depth-first search
class DFS:
    def __init__ (self, graph: nx.DiGraph, initial_node):
        self.graph = graph
        self.initial_node = initial_node
        self.parent = dict()
        self.time = 0
        self.starting_time = { node: -1 for node in graph.nodes() }
        self.ending_time = { node: -1 for node in graph.nodes() }
        self.search()
        self.post_processing()

    def search(self):
        if self.initial_node not in self.parent.keys():
            self.parent[self.initial_node] = -1
            self.visit(self.initial_node)
        for node in self.graph.nodes():
            if node not in self.parent.keys():
                self.parent[node] = -1
                self.visit(node)
        return

    def visit(self, node):
        self.time = self.time + 1
        self.starting_time[node] = self.time
        for child_node in graph.successors(node):
            if child_node not in self.parent.keys():
                self.parent[child_node] = node
                self.visit(child_node)
        self.time = self.time + 1
        self.ending_time[node] = self.time
        return

    def post_processing(self):
        self.times = {
            node: [self.starting_time[node], self.ending_time[node]]
            for node in self.graph.nodes()
        }
        self.edge_type = {
            edge: self._find_edge_type(edge)
            for edge in self.graph.edges()
        }
        return
    
    def _find_edge_type(self, edge):
        source_node = edge[0]
        source_node_starting_time = self.starting_time[source_node]
        source_node_ending_time = self.ending_time[source_node]
        target_node = edge[1]
        target_node_starting_time = self.starting_time[target_node]
        target_node_ending_time = self.ending_time[target_node]
        # forward
        if (source_node_starting_time < target_node_starting_time) and (source_node_ending_time > target_node_ending_time):
            return "forward"
        elif (source_node_starting_time > target_node_starting_time) and (source_node_ending_time < target_node_ending_time):
            return "back"
        elif (source_node_ending_time < target_node_starting_time) or (source_node_starting_time > target_node_ending_time):
            return "cross"
        else:
            return "impossible"

    def save(self):
        node_times = pd.DataFrame(
            list(map(
                lambda x: [node_map[x[0]], x[0], x[1][0], x[1][1]],
                sorted(self.times.items(), key = lambda x: x[0])
            )),
            columns = ["node name", "node number", "starting time", "ending time"]
        )
        node_times.to_csv(
            os.path.join(output_dir, "nodes.csv"),
            sep = ",",
            line_terminator = "\n",
            index = False
        )
        edge_types_df = pd.DataFrame(
            list(map(
                lambda x: [x[0][0], x[0][1], x[1]],
                self.edge_type.items(),
            )),
            columns = ["source node number", "target node number", "edge type"]
        )
        edge_types_df.to_csv(
            os.path.join(output_dir, "edges.csv"),
            sep = ",",
            line_terminator = "\n",
            index = False
        )
        return

dfs = DFS(graph, initial_node)
dfs.save()
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

def make_cayley_tree(degree: int, depth: int):
        graph: nx.Graph = nx.Graph()
        graph.add_node(0)
        next_vertex = 1
        last_vertices_added = []
        if depth >= 1:
            for i in range(degree):
                last_vertices_added.append(next_vertex)
                graph.add_edge(0, next_vertex)
                next_vertex += 1
        current_depth = 2
        while current_depth <= depth:
            root_vertex_list = last_vertices_added
            last_vertices_added = []
            for root in root_vertex_list:
                for i in range(degree - 1):
                    last_vertices_added.append(next_vertex)
                    graph.add_edge(root, next_vertex)
                    next_vertex += 1
            current_depth += 1
        return graph


class CayleyTree:

    def __init__ (self, degree: int, depth: int):
        self.degree: int = degree
        self.depth: int = depth
        self.graph: nx.Graph = make_cayley_tree(self.degree, self.depth)
        return
    
    def draw(self):
        pos = graphviz_layout(self.graph, prog="twopi")
        nx.draw(self.graph, pos)
        plt.savefig("foo.png")

if __name__ == "__main__":
    tree = CayleyTree(4, 3)
    tree.draw()
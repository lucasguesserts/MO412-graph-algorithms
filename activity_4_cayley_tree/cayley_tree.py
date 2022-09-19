import os
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

def make_cayley_tree(degree: int, depth: int) -> nx.Graph:
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
    
    def draw(self) -> None:
        # https://stackoverflow.com/questions/57512155/how-to-draw-a-tree-more-beautifully-in-networkx
        pos = graphviz_layout(self.graph, prog="twopi")
        nx.draw(self.graph, pos)
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(
            output_dir,
            f"cayley_tree_k_{self.degree}_P_{self.depth}.png",
        ))
    
    @property
    def diameter(self) -> int:
        return nx.diameter(self.graph)
    
    @property
    def number_of_nodes(self) -> int:
        return self.graph.number_of_nodes()

    def summarize(self):
        print(f"Cayley Tree:")
        print(f"\tTree parameters:")
        print(f"\t\tdegree (k) = {self.degree}")
        print(f"\t\tdepth (P) = {self.depth}")
        print(f"\tTree properties:")
        print(f"\t\tdiameter - d_max(k,P) = {self.diameter}")
        print(f"\t\tnumber of nodes - N(k,P) = {self.number_of_nodes}")
        print("") 

class CayleyTreeProps:

    def __init__ (self, degree: int, depth: int):
        self.degree: int = degree
        self.depth: int = depth
        return
    
    @property
    def diameter(self) -> int:
        return 2 * self.depth
    
    @property
    def number_of_nodes(self) -> int:
        return int(1 + self.degree * ((self.degree - 1)**self.depth - 1) / (self.degree - 2))

    def summarize(self):
        print(f"Cayley Tree - closed formulas:")
        print(f"\tTree parameters:")
        print(f"\t\tdegree (k) = {self.degree}")
        print(f"\t\tdepth (P) = {self.depth}")
        print(f"\tTree properties:")
        print(f"\t\tdiameter - d_max(k,P) = {self.diameter}")
        print(f"\t\tnumber of nodes - N(k,P) = {self.number_of_nodes}")
        print("")

if __name__ == "__main__":
    degree = 4
    depth = 3
    tree = CayleyTree(
        degree = degree,
        depth = depth
    )
    props = CayleyTreeProps(
        degree = degree,
        depth = depth
    )
    tree.draw()
    tree.summarize()
    props.summarize()
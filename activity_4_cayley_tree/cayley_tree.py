import os
import json
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Helvetica"
})

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

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
        plt.savefig(os.path.join(
            output_dir,
            f"cayley_tree_k_{self.degree}_P_{self.depth}.png",
        ))
        plt.close()
        return
    
    @property
    def diameter(self) -> int:
        return nx.diameter(self.graph)
    
    @property
    def number_of_nodes(self) -> int:
        return self.graph.number_of_nodes()

    def summarize(self) -> None:
        print(f"Cayley Tree:")
        print(f"\tTree parameters:")
        print(f"\t\tdegree (k) = {self.degree}")
        print(f"\t\tdepth (P) = {self.depth}")
        print(f"\tTree properties:")
        print(f"\t\tdiameter - d_max(k,P) = {self.diameter}")
        print(f"\t\tnumber of nodes - N(k,P) = {self.number_of_nodes}")
        print("")
        return

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

    def summarize(self) -> None:
        print(f"Cayley Tree - closed formulas:")
        print(f"\tTree parameters:")
        print(f"\t\tdegree (k) = {self.degree}")
        print(f"\t\tdepth (P) = {self.depth}")
        print(f"\tTree properties:")
        print(f"\t\tdiameter - d_max(k,P) = {self.diameter}")
        print(f"\t\tnumber of nodes - N(k,P) = {self.number_of_nodes}")
        print("")
        return

class NDplot:

    def __init__(self, file_path: str, student_id: str):
        with open(file_path, "r") as file:
            data = json.load(file)
        self.degree = data[student_id]
        self.max_depth = 10
        return

    def _summarize_curve_fit(self, x_name, x, y_name, y):
        function = lambda x, alpha, beta: alpha * np.log(x) + beta
        popt, pcov = scipy.optimize.curve_fit(function, x, y)
        perr = np.sqrt(np.diag(pcov))
        alpha = popt[0]
        alpha_error = perr[0]
        beta = popt[1]
        beta_error = perr[1]
        print(f"Curve fit:")
        print(f"\t{y_name} = f({x_name}) = alpha * ln({x_name}) + beta")
        print(f"\talpha = {alpha} +- {alpha_error}")
        print(f"\tbeta = {beta} +- {beta_error}")
        print("")
        return lambda x: alpha * np.log(x) + beta

    def plot(self) -> None:
        depth_values = np.arange(1, self.max_depth + 1, 1)
        number_of_nodes_array = np.array(list(map(
            lambda d: CayleyTreeProps(degree = self.degree, depth = d).number_of_nodes,
            depth_values
        )))
        diameter_array = np.array(list(map(
            lambda d: CayleyTreeProps(degree = self.degree, depth = d).diameter,
            depth_values
        )))
        curve = self._summarize_curve_fit("N", number_of_nodes_array, "d_{max}", diameter_array)
        print(f"Plot:")
        print(f"\tdepth_values = {depth_values}")
        print(f"\tnumber_of_nodes_array = {number_of_nodes_array}")
        print(f"\tdiameter_array = {diameter_array}")
        plt.plot(np.log(number_of_nodes_array), diameter_array, color="k", linestyle="-", marker=".", label="values")
        # plt.plot(np.log(number_of_nodes_array), curve(number_of_nodes_array), color="gray", linestyle="--", label="curve fit")
        plt.title(r"$d_{\max}(k, P)$ and $ln(N(k, P))$, for $P$ ranging from $1$ to $10$")
        plt.xlabel(r"$ln(N(k, P))$")
        plt.ylabel(r"$d_{\max}(k, P)$")
        plt.grid(True)
        plt.legend(loc="best")
        plt.savefig(os.path.join(
            output_dir,
            f"diameter_as_a_function_of_the_number_of_nodes.png",
        ))
        plt.close()
        return

if __name__ == "__main__":
    degree = 3
    depth = 5
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
    nd_plot = NDplot("./k.json", "LG")
    nd_plot.plot()
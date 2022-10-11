import itertools
import os
import pickle

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class BarabasiAlbertGraph:
    def __init__(
        self,
        initial_number_of_nodes: int,
        number_of_generations: int,
        checkpoint_list: list[int],
    ):
        self.initial_number_of_nodes: int = initial_number_of_nodes
        self.number_of_edges_for_new_nodes: int = initial_number_of_nodes
        self._init_graph()
        self._init_checkpoints(checkpoint_list)
        for _ in range(number_of_generations):
            self._evolve_graph()
            self._mark_checkpoint()
        return

    def _init_graph(self) -> None:
        self.initial_edge_list = list(
            itertools.combinations(range(self.initial_number_of_nodes), 2)
        )
        self.graph: nx.Graph = nx.Graph()
        for edge in self.initial_edge_list:
            self.graph.add_edge(*edge)
        return

    def _init_checkpoints(self, checkpoint_list: list[int]) -> None:
        self.checkpoint: dict[int, nx.Graph] = dict()
        for checkpoint in checkpoint_list:
            self.checkpoint[checkpoint] = None
        return

    def _evolve_graph(self) -> None:
        next_node: int = self.graph.number_of_nodes()
        print(next_node)
        node_degree_pair_list: list[(int, int)] = self.graph.degree
        degree_sum: int = sum(map(lambda pair: pair[1], node_degree_pair_list))
        node_probability_pair_list: list[(int, int)] = list(
            map(lambda pair: (pair[0], pair[1] / degree_sum), node_degree_pair_list)
        )
        nodes_to_connect: list[int] = np.random.choice(
            list(map(lambda pair: pair[0], node_probability_pair_list)),
            self.number_of_edges_for_new_nodes,
            replace=False,
            p=list(map(lambda pair: pair[1], node_probability_pair_list)),
        )
        for node_in_graph in nodes_to_connect:
            self.graph.add_edge(next_node, node_in_graph)
        return

    def _mark_checkpoint(self):
        number_of_nodes: int = self.graph.number_of_nodes()
        if number_of_nodes in self.checkpoint.keys():
            self.checkpoint[number_of_nodes] = self.graph.copy()
        return

    def save_checkpoints(self, output_dir: str) -> None:
        for number_of_nodes, graph in self.checkpoint.items():
            file_name: str = os.path.join(
                output_dir,
                f"{number_of_nodes}.pkl"
            )
            print(f"Saving checkpoint with {number_of_nodes} nodes in '{file_name}'")
            with open(file_name, "wb") as file:
                pickle.dump(graph, file)
        return


class Expected:
    @staticmethod
    def number_of_edges(
        initial_number_of_edges: int,
        number_of_edges_added_per_generation: int,
        number_of_generations: int,
    ) -> int:
        return (
            initial_number_of_edges
            + number_of_generations * number_of_edges_added_per_generation
        )

    @staticmethod
    def number_of_nodes(
        initial_number_of_nodes: int, number_of_generations: int
    ) -> int:
        return initial_number_of_nodes + number_of_generations

    @staticmethod
    def all_assertions(model: BarabasiAlbertGraph):
        expected_number_of_nodes: int = Expected.number_of_nodes(
            initial_number_of_nodes, number_of_generations
        )
        expected_number_of_edges: int = Expected.number_of_edges(
            len(list(itertools.combinations(range(initial_number_of_nodes), 2))),
            initial_number_of_nodes,
            number_of_generations,
        )
        assert model.graph.number_of_edges() == expected_number_of_edges
        assert model.graph.number_of_nodes() == expected_number_of_nodes



if __name__ == "__main__":
    output_dir = os.path.join(os.path.abspath(os.getcwd()), "output")
    os.makedirs(output_dir, exist_ok=True)

    initial_number_of_nodes: int = 4
    number_of_generations: int = 10_000
    checkpoint_list: list[int] = [100, 1_000, 10_000]

    model = BarabasiAlbertGraph(
        initial_number_of_nodes,
        number_of_generations,
        checkpoint_list,
    )

    model.save_checkpoints(output_dir)

    Expected.all_assertions(model)




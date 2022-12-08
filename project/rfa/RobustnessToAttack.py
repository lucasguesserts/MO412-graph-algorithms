import pickle

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class RobustnessToAttack:
    def __init__(self, g: nx.MultiDiGraph):
        self.N = g.number_of_nodes()
        self.g = g.copy()
        self.ps = []
        self.fs = []
        self._run()
        self.ps = np.array(self.ps)
        self.fs = np.array(self.fs)
        return

    @staticmethod
    def from_pickle(file_name):
        with open(file_name, "rb") as file:
            obj = pickle.load(file)
        return obj

    def save(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self, file)
        return

    # def plot(self, ax: plt.Axes, tail_cut: int, mark_critical_threshold: bool) -> None:
    #     ax.plot(self.fs[:-tail_cut], self.ps[:-tail_cut], 'k', label="attacks")
    #     if mark_critical_threshold:
    #         f_critical = self._find_critical_threshold()
    #         ax.vlines(f_critical, 0, 1, color='gray', linestyles='--', label="fc = {:.2f}".format(f_critical))
    #     return

    def _compute_p_inf(self) -> float:
        components = nx.weakly_connected_components(self.g)
        largest_component = max(components, key=lambda c: len(c))
        return len(largest_component) / self.g.number_of_nodes()

    def _find_main_node(self):
        return max(self.g.nodes(), key=lambda n: self.g.degree(n))

    def _compute_f(self) -> float:
        return 1 - (self.g.number_of_nodes() / self.N)

    def _run(self):
        while self.g.number_of_nodes() > 1:
            n = self._find_main_node()
            self.g.remove_node(n)
            self.ps.append(self._compute_p_inf())
            self.fs.append(self._compute_f())
            print(self.g.number_of_nodes())
        return

    # def _find_critical_threshold(self):
    #     for i in range(len(self.ps)):
    #         if self.ps[i] < 0.01:
    #             break
    #     f_critical = self.fs[i]
    #     return f_critical

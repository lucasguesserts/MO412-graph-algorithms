from typing import Callable, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import numpy.typing as npt

from .DegreeType import DegreeType
from .RobustnessToAttack import RobustnessToAttack
from .WikiData import WikiData
from .WikiDataGraphMaker import WikiDataGraphMaker


class GraphPerYear:
    def __init__(self, data: list[WikiData], build_robustness: bool = False):
        self._raw_data = data.copy()
        self._year_list = self._make_year_list()
        self._data = self._make_data()
        if build_robustness:
            self.robustness = {
                year: RobustnessToAttack(self._data[year]) for year in self._year_list
            }

    def _make_year_list(self) -> list[int]:
        return list(
            range(
                GraphPerYear._minimum_year(self._raw_data),
                GraphPerYear._maximum_year(self._raw_data) + 1,
            )
        )

    def _make_data(self) -> dict[int, nx.MultiDiGraph]:
        d = {
            year: GraphPerYear._make_graph(self._raw_data, year)
            for year in self._year_list
        }
        return d

    def plot(
        self, ax: plt.Axes, f: Callable[[float], nx.MultiDiGraph], y_label: str = ""
    ) -> None:
        x = self._data.keys()
        y = list(map(f, self._data.values()))
        ax.plot(x, y, color="black", marker="o")
        ax.set_xlim([min(self._year_list), max(self._year_list)])
        ax.set_ylabel(y_label)
        ax.set_xlabel("year")
        ax.set_xticks(self._year_list)
        ax.grid(visible=True, axis="x", which="major")
        ax.grid(visible=True, axis="y", which="major")
        return

    def plot_quartiles(
        self,
        ax: plt.Axes,
        degree_type: DegreeType = DegreeType.OUT,
        outliers: bool = False,
    ) -> None:
        x = self._data.keys()
        y = list(
            map(
                lambda g: GraphPerYear._get_graph_degree(g, degree_type),
                self._data.values(),
            )
        )
        ax.boxplot(
            y,
            labels=x,
            vert=False,
            showfliers=outliers,
        )
        degree_type_str = degree_type.__str__().split(".")[-1].title()
        ax.set_title(f"{degree_type_str}-Degree Quartiles per Year (without outliers)")
        ax.set_xlabel(f"{degree_type_str}-Degree")
        ax.set_ylabel("Year")
        ax.grid(True, alpha=0.4)
        return

    @staticmethod
    def _get_graph_degree(
        graph: nx.MultiDiGraph, degree_type: DegreeType = DegreeType.OUT
    ) -> npt.NDArray[np.int_]:
        graph_node_degree_function = (
            graph.out_degree if degree_type == DegreeType.OUT else graph.in_degree
        )
        degrees = np.array(list(map(lambda x: x[1], graph_node_degree_function(graph))))
        return degrees

    @staticmethod
    def _make_graph(data: list[WikiData], year: int) -> nx.MultiDiGraph:
        graph_maker = WikiDataGraphMaker()
        graph_maker.data = data
        year_filter_criteria = lambda data: list(
            filter(lambda wd: wd.year == year, data)
        )
        graph_maker.add_filter(year_filter_criteria)
        graph = graph_maker.make()
        return graph

    @staticmethod
    def _minimum_year(data: list[WikiData]) -> int:
        return min(map(lambda wd: wd.year, data))

    @staticmethod
    def _maximum_year(data: list[WikiData]) -> int:
        return max(map(lambda wd: wd.year, data))

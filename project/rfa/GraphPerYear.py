import networkx as nx
import matplotlib.pyplot as plt

from typing import Callable

from .WikiData import WikiData
from .WikiDataGraphMaker import WikiDataGraphMaker


class GraphPerYear:
    def __init__(self, data: list[WikiData]):
        self._raw_data = data.copy()
        self._year_list = self._make_year_list()
        self._data = self._make_data()

    def _make_year_list(self) -> list[int]:
        return list(
            range(
                GraphPerYear._minimum_year(self._raw_data),
                GraphPerYear._maximum_year(self._raw_data) + 1,
            )
        )

    def _make_data(self):
        d: dict[int, nx.MultiDiGraph] = {
            year: GraphPerYear._make_graph(self._raw_data, year)
            for year in self._year_list
        }
        return d

    def plot(self, ax: plt.Axes, f: Callable[[float], nx.MultiDiGraph], y_label: str = "") -> None:
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
    def _minimum_year(data: list[WikiData]):
        return min(map(lambda wd: wd.year, data))

    @staticmethod
    def _maximum_year(data: list[WikiData]):
        return max(map(lambda wd: wd.year, data))

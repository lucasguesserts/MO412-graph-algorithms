from typing import Callable

import networkx as nx

from .WikiData import WikiData


class WikiDataGraphMaker:

    _basic_filter_criterias: list[Callable[[list[WikiData]], list[WikiData]]] = [
        lambda data: list(filter(lambda wd: wd.vote != 0, data)),
    ]

    def __init__(self) -> None:
        self._data: list[WikiData] = []
        self._filters = self._basic_filter_criterias.copy()
        return

    @property
    def data(self) -> list[WikiData]:
        return self._data.copy()

    @data.setter
    def data(self, data: list[WikiData]) -> None:
        self._data = data
        return

    def add_filter(
        self, filter_criteria: Callable[[list[WikiData]], list[WikiData]]
    ) -> None:
        self._filters.append(filter_criteria)
        return

    def make(self) -> nx.MultiDiGraph:
        graph = nx.MultiDiGraph()
        data = self._apply_filters(self.data)
        for wd in data:
            graph.add_edge(wd.source, wd.target, weight=wd.vote)
        return graph

    def _apply_filters(self, data: list[WikiData]) -> list[WikiData]:
        for filter_criteria in self._filters:
            data = filter_criteria(data)
        return data

from typing import Callable

import networkx as nx


class WikiDataException(Exception):
    def __init__(self, original_data: dict[str, str], message: str):
        Exception.__init__(self, message)
        self.data = original_data
        return

    def __str__(self):
        return {"message": Exception.__str__(self), "data": self.data}.__str__()


class WikiData:
    def __init__(self, data: dict[str, str]) -> None:
        self.source: str = str(data["SRC"])
        self.target: str = str(data["TGT"])
        self.vote: int = int(data["VOT"])
        self.accepted: bool = int(data["RES"]) == 1
        self.year: int = int(data["YEA"])
        self.comment: str = str(data["TXT"])
        self._validate(data)
        return

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "vote": self.vote,
            "accepted": self.accepted,
            "year": self.year,
            "comment": self.comment,
        }

    def __str__(self) -> str:
        return self.to_dict().__str__()

    def _validate(self, data) -> None:
        if self.source == "":
            raise WikiDataException(data, "no source provided")
        if self.target == "":
            raise WikiDataException(data, "no target provided")
        if (self.vote != -1) and (self.vote != 0) and (self.vote != 1):
            raise WikiDataException(data, "invalid vote")
        if (self.year < 2003) or (self.year > 2013):
            raise WikiDataException(data, "invalid year")
        return


class WikiDataReader:
    number_of_data_lines = 7

    @property
    def data(self) -> list[WikiData]:
        return self._wiki_data_list

    @property
    def exceptions(self) -> list[WikiDataException]:
        return self._exceptions

    def __init__(self, file_name):
        self._file_name = file_name
        self._wiki_data_read = False
        self._wiki_data_list = []
        self._exceptions = []
        self._read()
        return

    def __str__(self):
        s = ""
        for d in self.data:
            s += d.__str__() + "\n"
        for d in self.exceptions:
            s += d.__str__() + "\n"
        return s

    def _read(self) -> None:
        wiki_data_list = []
        with open(self._file_name) as file:
            while True:
                lines = [
                    file.readline().strip()
                    for _ in range(WikiDataReader.number_of_data_lines)
                ]
                file.readline()  # drop the empty line
                if lines[0] == "":
                    break
                raw_wiki_data = self._data_list_to_dict(lines)
                try:
                    wiki_data = WikiData(raw_wiki_data)
                    wiki_data_list.append(wiki_data)
                except WikiDataException as exception:
                    self._exceptions.append(exception)
        self._wiki_data_list = wiki_data_list
        self._wiki_data_read = True
        return

    def _data_list_to_dict(self, data: list[str]) -> dict[str, str]:
        data = dict(map(lambda s: s.split(":", 1), data))
        return data


class WikiDataGraphMaker:
    def __init__(self, wiki_data_list: list[WikiData]) -> None:
        self.wiki_data_list: list[WikiData] = wiki_data_list
        self._filter_list()
        return

    def make(self) -> nx.MultiDiGraph():
        graph = nx.MultiDiGraph()
        for wd in self.wiki_data_list:
            graph.add_edge(wd.source, wd.target, weight=wd.vote)
        return graph

    _filter_criterias: list[Callable[[list[WikiData]], list[WikiData]]] = [
        lambda wiki_data_list: list(
            filter(lambda wiki_data: wiki_data.vote != 0, wiki_data_list)
        )
    ]

    def _filter_list(self) -> list[WikiData]:
        for filter_criteria in self._filter_criterias:
            self.wiki_data_list = filter_criteria(self.wiki_data_list)
        return self.wiki_data_list

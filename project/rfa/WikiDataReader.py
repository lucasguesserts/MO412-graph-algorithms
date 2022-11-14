from .WikiData import WikiData
from .exception import WikiDataException

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

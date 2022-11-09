from datetime import datetime
import re


class WikiDataException(Exception):
    def __init__(self, original_data: dict[str, str], message: str):
        Exception.__init__(self, message)
        self.data = original_data
        return

    def __str__(self):
        return {"message": Exception.__str__(self), "data": self.data}.__str__()


class DatetimeConverter:
    @staticmethod
    def convert(text) -> datetime:
        regex = r"^(\d{2}):(\d{2}), (\d{1,2}) ([A-Z][a-z]+) (\d{4})$"
        x = re.match(regex, text)
        x = x.groups()
        return datetime(
            year=int(x[4]),
            month=DatetimeConverter._month_to_int[x[3]],
            day=int(x[2]),
            hour=int(x[0]),
            minute=int(x[1]),
        )

    _month_to_int: dict[str, int] = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }


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
            "date": self.date.isoformat(),
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

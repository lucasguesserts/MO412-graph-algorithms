from .exception import WikiDataException


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

class WikiDataException(Exception):
    def __init__(self, original_data: dict[str, str], message: str):
        Exception.__init__(self, message)
        self.data = original_data
        return

    def __str__(self):
        return {"message": Exception.__str__(self), "data": self.data}.__str__()

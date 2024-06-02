class CurrencyValues():
    def __init__(self, name: str, values: list[float]):
        self.name = name
        self.values = values

    def serialize(self):
        return {"name": self.name, "values": self.values}
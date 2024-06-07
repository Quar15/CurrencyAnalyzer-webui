from currency_analyzer.main.models import ExchangeRates

class CurrencyValues():
    def __init__(self, name: str, rates: list[ExchangeRates]|None):
        self.name = name
        self.values = []
        for rate in rates:
            if rate is None:
                self.values.append('ERROR')
            else:
                self.values.append(rate.rate)

    def serialize(self):
        return {"name": self.name, "values": self.values}
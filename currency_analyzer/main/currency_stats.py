from sqlalchemy import func
from currency_analyzer import db
from currency_analyzer.main.models import Currency, ExchangeRates


class CurrencyStats:
    def __init__(self, currency: Currency, from_date, to_date):
        self.currency = currency
        self.high = self._get_high(from_date, to_date)
        self.low = self._get_low(from_date, to_date)
        self.average = self._get_avg(from_date, to_date)
        self.change, self.change_perc = self._get_change(from_date, to_date)

    def _get_high(self, from_date, to_date) -> float:
        result = (db.session.query(func.max(ExchangeRates.rate))
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date.between(from_date, to_date)).first()
        )[0]
        if result is None:
            result = 0
        return result

    def _get_low(self, from_date, to_date) -> float:
        result = (db.session.query(func.min(ExchangeRates.rate))
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date.between(from_date, to_date)).first()
        )[0]
        if result is None:
            result = 0
        return result

    def _get_avg(self, from_date, to_date) -> float:
        result = (db.session.query(func.avg(ExchangeRates.rate))
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date.between(from_date, to_date)).first()
        )[0]
        if result is None:
            result = 0
        else:
            result = float(result)
        return result

    def _get_change(self, from_date, to_date) -> [float]:
        start_value_result = (ExchangeRates.query
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date >= from_date)
            .filter(ExchangeRates.date <= to_date)
            .order_by(ExchangeRates.date)
            .first()
        )
        end_value_result = (ExchangeRates.query
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date >= from_date)
            .filter(ExchangeRates.date <= to_date)
            .order_by(ExchangeRates.date.desc())
            .first()
        )
        if start_value_result is None:
            return 0, 0
        return end_value_result.rate - start_value_result.rate, ((end_value_result.rate - start_value_result.rate) / start_value_result.rate * 100.0)

    def serialize(self):
        return {
            "currency": self.currency.code,
            "high": self.high,
            "low": self.low,
            "avg": self.average,
            "change": self.change,
            "change_perc": self.change_perc,
        }

from datetime import date, timedelta
from sqlalchemy import func
from currency_analyzer import db
from currency_analyzer.main.models import Currency, ExchangeRates


class CurrencyStats:
    def __init__(self):
        self.high = 0
        self.low = 0
        self.average = 0
        self.change = 0
        self.change_perc = 0

    def init_from_currency(self, currency: Currency, from_date, to_date) -> 'CurrencyStats':
        self.currency = currency
        self.found_data_in_range: bool = self._has_data_in_range(from_date, to_date)
        if self.found_data_in_range:
            self.high = self._get_high(from_date, to_date)
            self.low = self._get_low(from_date, to_date)
            self.average = self._get_avg(from_date, to_date)
            self.change, self.change_perc = self._get_change(from_date, to_date)
        return self

    def init_from_data(self, currency: Currency, found_data_in_range: bool, high: float, low: float, average: float, change: float, change_perc: float) -> 'CurrencyStats':
        self.currency = currency
        self.found_data_in_range = found_data_in_range
        self.high = high
        self.low = low
        self.average = average
        self.change = change
        self.change_perc = change_perc
        return self

    def _has_data_in_range(self, from_date, to_date) -> bool:
        result = (ExchangeRates.query
            .filter(ExchangeRates.code == self.currency.code)
            .filter(ExchangeRates.date.between(from_date, to_date)).first()
        )
        return not result is None

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
            "found_data_in_range": 'true' if self.found_data_in_range else 'false',
            "high": self.high,
            "low": self.low,
            "avg": self.average,
            "change": self.change,
            "change_perc": self.change_perc,
        }


def _query_currency_stats(from_date: date, to_date: date) -> (dict, list[ExchangeRates], list[ExchangeRates]):
    max_min_avg_results = (
        db.session.query(
            ExchangeRates.code,
            func.max(ExchangeRates.rate),
            func.min(ExchangeRates.rate),
            func.avg(ExchangeRates.rate)
        )
        .filter(
            ExchangeRates.date.between(from_date, to_date)
        )
        .group_by(ExchangeRates.code)
        .order_by(ExchangeRates.code)
    ).all()

    earliest_rate_subquery = (
        db.session.query(
            ExchangeRates.code,
            func.min(ExchangeRates.date).label('min_date')
        )
        .filter(ExchangeRates.date.between(from_date, to_date))
        .group_by(ExchangeRates.code)
        .subquery()
    )
    earliest_rate_results = (
        db.session.query(ExchangeRates)
        .join(earliest_rate_subquery, (ExchangeRates.code == earliest_rate_subquery.c.code) & (ExchangeRates.date == earliest_rate_subquery.c.min_date))
        .order_by(ExchangeRates.code)
    ).all()

    oldest_rate_subquery = (
        db.session.query(
            ExchangeRates.code,
            func.max(ExchangeRates.date).label('max_date')
        )
        .filter(ExchangeRates.date.between(from_date, to_date))
        .group_by(ExchangeRates.code)
        .subquery()
    )
    oldest_rate_results = (
        db.session.query(ExchangeRates)
        .join(oldest_rate_subquery, (ExchangeRates.code == oldest_rate_subquery.c.code) & (ExchangeRates.date == oldest_rate_subquery.c.max_date))
        .order_by(ExchangeRates.code)
    ).all()

    return max_min_avg_results, earliest_rate_results, oldest_rate_results


def get_currency_stats() -> (list[Currency], dict):
    currencies = Currency.query.all()
    currency_stats_dict = {}
    print("PRE")
    max_min_avg_results, earliest_rate_results, oldest_rate_results = _query_currency_stats(date.today() - timedelta(days=30), date.today())
    print("POST")

    for i in range(len(max_min_avg_results)):
        change: float = oldest_rate_results[i].rate - earliest_rate_results[i].rate
        change_perc: float = change / earliest_rate_results[i].rate * 100.0
        currency_stats_dict[max_min_avg_results[i][0]] = CurrencyStats().init_from_data(
            currency=Currency.query.filter(Currency.code == max_min_avg_results[i][0]).first(),
            found_data_in_range=True,
            high=max_min_avg_results[i][1],
            low=max_min_avg_results[i][2], 
            average=max_min_avg_results[i][3],
            change=change,
            change_perc=change_perc,
        ).serialize()
    # There can be missing currencies that do not have data from last 30 days
    for currency in currencies:
        if currency.code not in currency_stats_dict.keys():
            currency_stats_dict[currency.code] = CurrencyStats().init_from_data(
                currency=currency,
                found_data_in_range=False,
                high=0.0,
                low=0.0, 
                average=0.0,
                change=0.0,
                change_perc=0.0,
            ).serialize()
    return currencies, currency_stats_dict
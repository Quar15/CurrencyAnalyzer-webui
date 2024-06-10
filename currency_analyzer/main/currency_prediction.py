from sqlalchemy import func
from currency_analyzer.main.models import Currency, ExchangeRatesPredictions
from currency_analyzer import db, cache


def get_latest_predictions_for_currencies(currencies: list[Currency]) -> list[ExchangeRatesPredictions]:
    currency_codes = [currency.code for currency in currencies]
    latest_prediction_subquery = (
        db.session.query(
            ExchangeRatesPredictions.code,
            func.min(ExchangeRatesPredictions.date).label('min_date')
        )
        .filter(ExchangeRatesPredictions.code.in_(currency_codes))
        .group_by(ExchangeRatesPredictions.code)
        .subquery()
    )

    latest_prediction_results = (
        db.session.query(ExchangeRatesPredictions)
        .join(latest_prediction_subquery, 
            (ExchangeRatesPredictions.code == latest_prediction_subquery.c.code) 
            & (ExchangeRatesPredictions.date == latest_prediction_subquery.c.min_date)
        )
        .order_by(ExchangeRatesPredictions.code)
    ).all()
    return latest_prediction_results



def get_latest_predictions_dict(currencies: list[Currency]) -> dict[ExchangeRatesPredictions]:
    latest_predictions_dict = {}
    currency_codes = [currency.code for currency in currencies]
    latest_predictions = get_latest_predictions_for_currencies(currencies)
    for i in range(len(latest_predictions)):
        latest_predictions_dict[latest_predictions[i].code] = latest_predictions[i]
    
    for code in currency_codes:
        if code not in latest_predictions_dict:
            latest_predictions_dict[code] = '-'

    return latest_predictions_dict
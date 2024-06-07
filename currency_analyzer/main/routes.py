import re
from flask import (
    render_template,
    Blueprint,
    request,
    url_for,
    make_response,
    flash,
    redirect,
    session,
)
from sqlalchemy import func
from datetime import datetime, timedelta, date
from currency_analyzer import db
from currency_analyzer.main.models import Currency, ExchangeRates
from currency_analyzer.main.utils import (
    add_notification_refresh_header,
    add_page_refresh_header,
    FLASH_MESSAGE_AVAILABLE_SESSION_VAR,
    REFRESH_PAGE_SESSION_VAR,
)
from currency_analyzer.main.currency_value import CurrencyValues
from currency_analyzer.main.currency_stats import CurrencyStats

main = Blueprint("main", __name__)
WATCHED_CURRENCY_SESSION_VAR = "watched_currencies"
TIMESTAMPS_FOR_ANALYZE_SESSION_VAR = "timestamp_for_analyze"
UPDATING_ANALYZE_ZOOM_SESSION_VAR = "updating_analyze_zoom"
ANALYZE_ZOOM_DAYS_SESSION_VAR = "analyze_zoom_days"
MIN_ZOOM_VALUE = 1
WATCHED_CURRENCY_LIMIT = 6
DATETIME_FORMAT = "%Y-%m-%d"


@main.route("/heartbeat")
def heartbeat():
    return ""

@main.route("/dev/clear")
def clear():
    session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR] = None
    session[ANALYZE_ZOOM_DAYS_SESSION_VAR] = 1
    session[UPDATING_ANALYZE_ZOOM_SESSION_VAR] = False
    return "OK"

@main.route("/notifications")
def notifications():
    return render_template("partials/notifications.html")


@main.route("/")
@add_notification_refresh_header
def index():
    return render_template('index.html', htmx_link_to_load=url_for('main.analyze'))


def normalize_date_based_on_zoom(date_to_normalize: date, zoom: int) -> date:
    if zoom == 7:
        while (date_to_normalize.weekday() != 0):
            date_to_normalize -= timedelta(days=1)
        return date_to_normalize
    elif zoom == 30:
        return date_to_normalize.replace(day=1)
    elif zoom == 365:
        return date_to_normalize.replace(month=1, day=1)
    return date_to_normalize


def get_labels_and_datetimes_in_timeframe(
    timestamp_since: date, timestamp_to: date, timedelta_days: int = 1
):
    labels = []
    datetimes = []
    
    x = normalize_date_based_on_zoom(timestamp_to, timedelta_days)
    target_timestamp = normalize_date_based_on_zoom(timestamp_since, timedelta_days)
    while x >= target_timestamp:
        x = normalize_date_based_on_zoom(x, timedelta_days)
        labels.append(date.strftime(x, DATETIME_FORMAT))
        datetimes.append(x)
        x -= timedelta(days=1)
    return labels, datetimes


def get_timestamps(request, earliest_timestamp) -> (date, date):
    datetime_pattern = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    timestamp_since = request.args.get("since", default=None)
    if timestamp_since is None or not datetime_pattern.match(timestamp_since):
        timestamp_since = date.today() - timedelta(days=30)
    else:
        timestamp_since = date.fromisoformat(timestamp_since)

    timestamp_to = request.args.get("to", default=None)
    if timestamp_to is None or not datetime_pattern.match(timestamp_to):
        timestamp_to = date.today() - timedelta(days=1)
    else:
        timestamp_to = date.fromisoformat(timestamp_to)

    if timestamp_since < earliest_timestamp:
        timestamp_since = earliest_timestamp

    if timestamp_to < timestamp_since:
        return (
            date.today() - timedelta(days=30),
            date.today() - timedelta(days=1)
        )

    return timestamp_since, timestamp_to


def agregate_values_to_zoom(currency_code: str, label_datetime: datetime, zoom: int) -> list[dict]:
    earlier_timestamp = normalize_date_based_on_zoom(label_datetime - timedelta(days=1), zoom)
    result = (db.session.query(func.avg(ExchangeRates.rate))
            .filter(ExchangeRates.code == currency_code)
            .filter(ExchangeRates.date.between(earlier_timestamp, label_datetime)).first()
    )[0]
    if result is None:
        return 'NO DATA'
    return float(result)


def get_currency_values_for_datetimes(currencies: list[Currency], datetimes: list[datetime], zoom: int) -> list[dict]:
    currency_values = []
    for currency in currencies:
        values = []
        if zoom > 1:
            for datetime in datetimes:
                values.append(agregate_values_to_zoom(currency.code, datetime, zoom))
            currency_values.append({"name": currency.code, "values": values})
        else:
            for datetime in datetimes:
                values.append(ExchangeRates.query.filter(ExchangeRates.code == currency.code).filter(ExchangeRates.date == datetime).one_or_none())
            currency_values.append(CurrencyValues(currency.code, values).serialize())
    return currency_values


def get_high_low_average_change_data_between_timestamps(currencies: list[Currency], from_date: datetime, to_date: datetime) -> list[dict]:
    currency_stats = []
    for currency in currencies:
        earliest_timestamp_for_currency = (ExchangeRates.query
            .filter(ExchangeRates.code == currency.code)
            .order_by(ExchangeRates.date)
            .first()
        ).date
        currency_stats.append(
            {
                "30days": CurrencyStats(currency, date.today() - timedelta(days=30), date.today()).serialize(),
                "90days": CurrencyStats(currency, date.today() - timedelta(days=90), date.today()).serialize(),
                "all": CurrencyStats(currency, earliest_timestamp_for_currency, date.today()).serialize(),
                "selected": CurrencyStats(currency, from_date, to_date).serialize(),
            }
        )
    return currency_stats


def is_zoom_being_updated() -> bool:
    return UPDATING_ANALYZE_ZOOM_SESSION_VAR in session and session[UPDATING_ANALYZE_ZOOM_SESSION_VAR]


@main.route("/analyze")
def analyze():
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        session[WATCHED_CURRENCY_SESSION_VAR] = []
    currencies = Currency.query.filter(
        Currency.id.in_(session[WATCHED_CURRENCY_SESSION_VAR])
    ).all()

    if not ANALYZE_ZOOM_DAYS_SESSION_VAR in session:
        session[ANALYZE_ZOOM_DAYS_SESSION_VAR] = 1
    zoom = session[ANALYZE_ZOOM_DAYS_SESSION_VAR]

    if is_zoom_being_updated():
        timestamp_since, timestamp_to = (
            datetime.strptime(session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR][0], DATETIME_FORMAT),
            datetime.strptime(session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR][1], DATETIME_FORMAT),
        )
        session[UPDATING_ANALYZE_ZOOM_SESSION_VAR] = False
    else:
        earliest_timestamp = (ExchangeRates.query
            .order_by(ExchangeRates.date)
            .first()
        ).date
        timestamp_since, timestamp_to = get_timestamps(request, earliest_timestamp)
        session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR] = (
            timestamp_since.strftime(DATETIME_FORMAT), 
            timestamp_to.strftime(DATETIME_FORMAT)
        )
    labels, datetimes = get_labels_and_datetimes_in_timeframe(timestamp_since, timestamp_to, zoom)
    currency_values = get_currency_values_for_datetimes(currencies, datetimes, zoom)
    currency_stats = get_high_low_average_change_data_between_timestamps(currencies, timestamp_since, timestamp_to)
    return render_template(
        "currency_analyze.html",
        labels=labels,
        currency_values=currency_values,
        currency_stats=currency_stats,
        since=timestamp_since.strftime(DATETIME_FORMAT),
        to=timestamp_to.strftime(DATETIME_FORMAT),
        zoom=zoom,
    )


@main.route("/analyze/zoom/<int:zoom>")
def analyze_zoom(zoom: int):
    session[UPDATING_ANALYZE_ZOOM_SESSION_VAR] = True
    if zoom < MIN_ZOOM_VALUE:
        zoom = MIN_ZOOM_VALUE
    session[ANALYZE_ZOOM_DAYS_SESSION_VAR] = zoom
    return redirect(url_for('main.analyze'))


@main.route("/list")
def currency_list():
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        session[WATCHED_CURRENCY_SESSION_VAR] = []
    currencies = Currency.query.all()
    serialized_watched_currencies = [
        c.serialize
        for c in Currency.query.filter(
            Currency.id.in_(session[WATCHED_CURRENCY_SESSION_VAR])
        ).all()
    ]
    return render_template(
        "currency_list.html",
        currencies=currencies,
        watched_currencies=serialized_watched_currencies,
        watched_currencies_ids=session[WATCHED_CURRENCY_SESSION_VAR],
    )


@main.route("/currency/watched/list")
@add_notification_refresh_header
@add_page_refresh_header
def currency_watch_list():
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        return render_template("partials/watch_list.html", watched_currencies=[])

    serialized_watched_currencies = [
        c.serialize
        for c in Currency.query.filter(
            Currency.id.in_(session[WATCHED_CURRENCY_SESSION_VAR])
        ).all()
    ]
    return render_template(
        "partials/watch_list.html", watched_currencies=serialized_watched_currencies
    )


@main.route("/currency/<int:currency_id>/list/row")
def currency_watch_list_row(currency_id: int):
    currency = Currency.query.get(currency_id)
    return render_template(
        "partials/currency_list_row.html",
        currency=currency,
        watched_currencies_ids=session[WATCHED_CURRENCY_SESSION_VAR],
    )


@main.route("/currency/watched/clear")
def currency_watch_list_clear():
    session[REFRESH_PAGE_SESSION_VAR] = True
    session[WATCHED_CURRENCY_SESSION_VAR] = []
    return redirect(url_for("main.currency_watch_list"))


@main.route("/currency/<int:currency_id>/watch")
def currency_watch(currency_id: int):
    currency = Currency.query.get(currency_id)
    session[FLASH_MESSAGE_AVAILABLE_SESSION_VAR] = True
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        session[WATCHED_CURRENCY_SESSION_VAR] = []
    if currency is None:
        flash("Currency not found")
        return redirect(url_for("main.currency_watch_list"))
    if currency_id in session[WATCHED_CURRENCY_SESSION_VAR]:
        flash(f"Currency '{currency.code}' is already set as watched")
        return redirect(url_for("main.currency_watch_list"))
    if len(session[WATCHED_CURRENCY_SESSION_VAR]) >= WATCHED_CURRENCY_LIMIT:
        flash("Cannot add more currencies")
        return redirect(url_for("main.currency_watch_list"))
    session[WATCHED_CURRENCY_SESSION_VAR].append(currency_id)
    flash(f"Added currency '{currency.code}' to watch list")
    return redirect(url_for("main.currency_watch_list"))


@main.route("/currency/<int:currency_id>/unwatch")
def currency_unwatch(currency_id: int):
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        session[WATCHED_CURRENCY_SESSION_VAR] = []
        return redirect(url_for("main.currency_watch_list"))
    currency = Currency.query.get(currency_id)
    if currency_id in session[WATCHED_CURRENCY_SESSION_VAR]:
        session[WATCHED_CURRENCY_SESSION_VAR].remove(currency_id)
        session[FLASH_MESSAGE_AVAILABLE_SESSION_VAR] = True
        flash(f"Currency '{currency.code}' removed from watch list")
    return redirect(url_for("main.currency_watch_list"))


@main.route("/currency/<int:currency_id>/unwatch/refresh")
def currency_unwatch_refresh(currency_id: int):
    session[REFRESH_PAGE_SESSION_VAR] = True
    return redirect(url_for("main.currency_unwatch", currency_id=currency_id))

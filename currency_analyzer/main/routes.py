import random # @TODO: Remove after implementing values in DB
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
from datetime import datetime, timedelta
from currency_analyzer.main.models import Currency
from currency_analyzer.main.utils import (
    add_notification_refresh_header,
    add_page_refresh_header,
    FLASH_MESSAGE_AVAILABLE_SESSION_VAR,
    REFRESH_PAGE_SESSION_VAR,
)
from currency_analyzer.main.currency_value import CurrencyValues

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


@main.route("/notifications")
def notifications():
    return render_template("partials/notifications.html")


@main.route("/")
@add_notification_refresh_header
def index():
    return render_template('index.html', htmx_link_to_load=url_for('main.analyze'))


def get_labels_and_datetimes_in_timeframe(
    timestamp_since: datetime, timestamp_to: datetime, timedelta_days: int = 1
):
    labels = []
    datetimes = []
    x = timestamp_to
    x = x.replace(hour=0, minute=0, second=0, microsecond=0)
    while x >= timestamp_since:
        labels.append(datetime.strftime(x, DATETIME_FORMAT))
        datetimes.append(x)
        x -= timedelta(days=timedelta_days)
    return labels, datetimes


def get_timestamps(request, earliest_timestamp):
    datetime_pattern = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    timestamp_since = request.args.get("since", default=None)
    if timestamp_since is None or not datetime_pattern.match(timestamp_since):
        timestamp_since = datetime.now() - timedelta(days=7)
    else:
        timestamp_since = datetime.strptime(timestamp_since, DATETIME_FORMAT)
    timestamp_since = timestamp_since.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamp_to = request.args.get("to", default=None)
    if timestamp_to is None or not datetime_pattern.match(timestamp_to):
        timestamp_to = datetime.now() - timedelta(days=1)
    else:
        timestamp_to = datetime.strptime(timestamp_to, DATETIME_FORMAT)
    timestamp_to = timestamp_to.replace(hour=0, minute=0, second=0, microsecond=0)

    if timestamp_since < earliest_timestamp:
        timestamp_since = earliest_timestamp

    if timestamp_to < timestamp_since:
        return (datetime.now() - timedelta(days=7)), (
            datetime.now() - timedelta(days=1)
        )

    return timestamp_since, timestamp_to


def get_currency_values_for_datetimes(currencies: list[Currency], datetimes: list[datetime]) -> list[CurrencyValues]:
    currency_values = []
    for currency in currencies:
        # @TODO: Query DB for data
        values = random.sample(range(1, 700), len(datetimes))
        currency_values.append(CurrencyValues(currency.name, values).serialize())
    return currency_values


def is_zoom_being_updated() -> bool:
    return UPDATING_ANALYZE_ZOOM_SESSION_VAR in session and session[UPDATING_ANALYZE_ZOOM_SESSION_VAR]


@main.route("/analyze")
def analyze():
    if not WATCHED_CURRENCY_SESSION_VAR in session:
        session[WATCHED_CURRENCY_SESSION_VAR] = []
    currencies = Currency.query.filter(
        Currency.id.in_(session[WATCHED_CURRENCY_SESSION_VAR])
    ).all()

    if ANALYZE_ZOOM_DAYS_SESSION_VAR in session:
        zoom = session[ANALYZE_ZOOM_DAYS_SESSION_VAR]

    if is_zoom_being_updated():
        timestamp_since, timestamp_to = session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR]
        session[UPDATING_ANALYZE_ZOOM_SESSION_VAR] = False
    else:
        timestamp_since, timestamp_to = get_timestamps(request, datetime.now() - timedelta(days=1400))
        session[TIMESTAMPS_FOR_ANALYZE_SESSION_VAR] = (timestamp_since, timestamp_to)
    labels, datetimes = get_labels_and_datetimes_in_timeframe(timestamp_since, timestamp_to, zoom)
    currency_values = get_currency_values_for_datetimes(currencies, datetimes)
    return render_template(
        "currency_analyze.html",
        labels=labels,
        currency_values=currency_values,
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
        flash(f"Currency '{currency.name}' is already set as watched")
        return redirect(url_for("main.currency_watch_list"))
    if len(session[WATCHED_CURRENCY_SESSION_VAR]) >= WATCHED_CURRENCY_LIMIT:
        flash("Cannot add more currencies")
        return redirect(url_for("main.currency_watch_list"))
    session[WATCHED_CURRENCY_SESSION_VAR].append(currency_id)
    flash(f"Added currency '{currency.name}' to watch list")
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
        flash(f"Currency '{currency.name}' removed from watch list")
    return redirect(url_for("main.currency_watch_list"))


@main.route("/currency/<int:currency_id>/unwatch/refresh")
def currency_unwatch_refresh(currency_id: int):
    session[REFRESH_PAGE_SESSION_VAR] = True
    return redirect(url_for("main.currency_unwatch", currency_id=currency_id))

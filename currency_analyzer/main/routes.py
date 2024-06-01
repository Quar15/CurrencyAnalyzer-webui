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
from currency_analyzer.main.models import Currency
from currency_analyzer.main.utils import (
    add_notification_refresh_header,
    add_page_refresh_header,
    FLASH_MESSAGE_AVAILABLE_SESSION_VAR,
    REFRESH_PAGE_SESSION_VAR,
)

main = Blueprint("main", __name__)
WATCHED_CURRENCY_SESSION_VAR = "watched_currencies"
WATCHED_CURRENCY_LIMIT_SESSION_VAR = 6


@main.route("/heartbeat")
def heartbeat():
    return ""


@main.route("/notifications")
def notifications():
    return render_template("partials/notifications.html")


@main.route("/")
@add_notification_refresh_header
def index():
    currency_values = [
        {"name": "PLN", "values": [1, 1, 2, 3, 4, 2, 9, 7, 8, 9]},
        {"name": "USD", "values": [9, 8, 7, 6, 5, 2, 1, 3, 5, 1]},
        {"name": "XYZ", "values": [2, 6, 5, 7, 4, 4, 5, 1, 1, 20]},
        {"name": "ABC", "values": [6, 5, 7, 4, 4, 5, 1, 1, 20, 2]},
        {"name": "DEF", "values": [5, 7, 4, 4, 5, 1, 1, 15, 2, 6]},
        {"name": "GHI", "values": [1, 1, 2, 6, 5, 7, 4, 4, 5, 13]},
    ]
    labels = [
        "2024-05-28 00:00:00",
        "2024-05-29 00:00:00",
        "2024-05-30 00:00:00",
        "2024-05-31 00:00:00",
        "2024-06-01 00:00:00",
        "2024-06-02 00:00:00",
        "2024-06-03 00:00:00",
        "2024-06-04 00:00:00",
    ]
    return render_template(
        "currency_analyze.html", labels=labels, currency_values=currency_values
    )


@main.route("/analyze")
def analyze():
    return redirect(url_for("main.index"))


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
    if len(session[WATCHED_CURRENCY_SESSION_VAR]) >= WATCHED_CURRENCY_LIMIT_SESSION_VAR:
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

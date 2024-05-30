from flask import render_template, Blueprint, request, url_for, make_response, flash, redirect

main = Blueprint("main", __name__)


@main.route("/heartbeat")
def heartbeat():
    return ""


@main.route("/")
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
    return redirect(url_for('main.index'))


@main.route("/list")
def currency_list():
    return render_template("currency_list.html")

FROM python:3.11-slim-buster

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt .env ./
COPY currency_analyzer currency_analyzer

RUN pip install -r requirements.txt
RUN apt update && apt -y install libpq-dev gcc && pip install psycopg2

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
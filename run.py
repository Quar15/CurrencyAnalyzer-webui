from currency_analyzer import create_app
import os

app = create_app(os.getenv("CURRENCY_ANALYZER_APP_CONFIG", "currency_analyzer.config.DevelopmentConfig"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
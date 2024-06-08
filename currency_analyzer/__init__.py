from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from currency_analyzer.config import Config

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    from currency_analyzer.main.routes import main
    from currency_analyzer.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
from currency_analyzer import db


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    image_path = db.Column(db.String(255), unique=False, nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'code': self.code,
            'image_path': self.image_path
        }


class ExchangeRates(db.Model):
    __tablename__ = 'exchange_rates_partitioned'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    rate = db.Column(db.Float())
    date = db.Column(db.Date)


class ExchangeRatesPredictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    prediction = db.Column(db.Float())
    date = db.Column(db.Date)
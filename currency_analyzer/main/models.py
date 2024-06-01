from currency_analyzer import db


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True, nullable=False)
    image_path = db.Column(db.String(255), unique=False, nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path
        }
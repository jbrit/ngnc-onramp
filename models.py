from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wallet(db.Model):
    address = db.Column(db.String, primary_key=True, nullable=False)
    payment_page_slug = db.Column(db.String, unique=True, nullable=False)
    payment_page_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<Wallet {}>'.format(self.address)

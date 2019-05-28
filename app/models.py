from app import app, db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    imageURL = db.Column(db.String(50))
    price = db.Column(db.Float, precision=2)
    desc = db.Column(db.String(200))
    amount = db.Column(db.Integer)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, precision=2)
    date_purchased = db.Column(db.DateTime, default=datetime.now().date())

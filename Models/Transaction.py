from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    # Unique ID for the transaction
    # -> primary key for the model
    transaction_id = db.Column(
        db.Integer, primary_key=True)
    # Date the transaction was made
    transaction_date = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # The first day the listing is booked for
    transaction_start_of_stay = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # The last day the listing is booked for
    transaction_end_of_stay = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # The amount the user paid
    transaction_cost = db.Column(
        db.Float, nullable=False)
    # The user ID of the person renting the property
    transaction_renter_id = db.Column(
        db.Integer, nullable=False)
    # The user id of the person who owns the property
    transaction_owner_id = db.Column(
        db.Integer, nullable=False)
    # The ID of the listing being booked
    transaction_listing_id = db.Column(
        db.Integer, nullable=False)

    def __repr__(self):
        return '<Transaction %r>' % self.transaction_id

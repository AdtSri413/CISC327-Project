from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import func
import User
import Listing
import Transaction

# setting up SQLAlchemy and data models so we can map data models into
# database tables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Review(db.Model):
    '''
    Description: Definition of the Review model
    '''
    # Unique ID of review
    # -> Primary key of the table
    review_id = db.Column(db.Integer, primary_key=True)
    # Review message
    review_message = db.Column(db.String(140), unique=False, nullable=False)
    # Date of review creation
    review_date = db.Column(
        db.DateTime, server_default=func.now(), unique=False, nullable=False)
    # Review score
    review_score = db.Column(db.Float(), unique=False, nullable=False)
    # ID of the user that made the review
    review_user_id = db.Column(db.Integer, SQLAlchemy.ForeignKey(
        User.user_id), unique=False, nullable=False)
    # Transaction ID that the review belong to
    review_transaction_id = db.Column(db.Integer, SQLAlchemy.ForeignKey(
        Listing.transaction_id), unique=False, nullable=False)
    # Listing ID that the review belong to
    review_listing_id = db.Column(db.Integer, SQLAlchemy.ForeignKey(
        Transaction.transaction_id), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

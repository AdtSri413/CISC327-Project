from qbnb import app
from flask_sqlalchemy import SQLAlchemy

'''
This file defines data models and related business logics
'''

db = SQLAlchemy(app)


class User(db.Model):
    '''
    Description: Definition of the User model
    '''
    # Unique ID of the user
    # -> primary key of the model
    user_id = db.Column(db.Integer, primary_key=True)
    # First Name of the user
    user_first_name = db.Column(db.String(120), unique=False, nullable=False)
    # Last Name of the user
    user_last_name = db.Column(db.String(120), unique=False, nullable=False)
    # Email Address of the user
    # -> must be unique since one email can only open one account
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    # Username of the user's account -> must be unique to identify each account
    user_username = db.Column(db.String(120), unique=True, nullable=False)
    # Password of the user's account -> doesn't have to be unique
    user_password = db.Column(db.String(120), unique=False, nullable=False)
    # Account Balance
    user_account_balance = db.Column(db.Float, unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username


class Listing(db.Model):
    '''
    Description: Definition of the Listing model
    '''
    # Unique ID of the listing
    # -> primary key of the model
    listing_id = db.Column(db.Integer, primary_key=True)
    # Name of the listing
    listing_name = db.Column(db.String(120), unique=False, nullable=False)
    # Address of the listing
    # -> must be unique since one address can only have one listing
    listing_address = db.Column(db.String(120), unique=True, nullable=False)
    # Daily price of the listing
    listing_price = db.Column(db.Float, unique=False, nullable=False)
    # Average Customer Rating
    listing_score = db.Column(db.Float, unique=False, nullable=False)
    # Unique ID of the owner
    # -> primary key of owner
    listing_owner_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Listing %r>' % self.listing_name


class Transaction(db.Model):
    '''
    Description: Definition of the Transaction model
    '''
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
        db.DateTime(timezone=True), unique=False, nullable=False)
    # Review score
    review_score = db.Column(db.Float(), unique=False, nullable=False)
    # ID of the user that made the review
    review_user_id = db.Column(db.Integer, unique=False, nullable=False)
    # Transaction ID that the review belong to
    review_transaction_id = db.Column(db.Integer, unique=False, nullable=False)
    # Listing ID that the review belong to
    review_listing_id = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Review %r>' % self.review_id


# create all tables
db.create_all()


# Put Assignment 2 functions here
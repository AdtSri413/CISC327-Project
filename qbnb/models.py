from queue import Empty
from random import randint
from qbnb import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    id = db.Column(db.Integer, primary_key=True)
    # Email Address of the user
    # -> must be unique since one email can only open one account
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Username of the user's account -> must be unique to identify each account
    username = db.Column(db.String(120), unique=True, nullable=False)
    # Password of the user's account -> doesn't have to be unique
    password = db.Column(db.String(120), unique=False, nullable=False)
    billing_address = db.Column(db.String(120), unique=False, nullable=False)
    postal_code = db.Column(db.String(6), unique=False, nullable=False)
    # Account Balance
    account_balance = db.Column(db.Float, unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username


class Listing(db.Model):
    '''
    Description: Definition of the Listing model
    '''
    # Unique ID of the listing
    # -> primary key of the model
    id = db.Column(db.Integer, primary_key=True)
    # Name of the listing
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Address of the listing
    # -> must be unique since one address can only have one listing
    description = db.Column(db.String(2000), nullable=False)
    # Daily price of the listing
    price = db.Column(db.Float, unique=False, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    user_email = db.Column(db.String(80), nullable=False,)
    # Unique ID of the owner
    # -> primary key of owner
    user_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Listing %r>' % self.id


class Booking(db.Model):
    '''
    Description: Definition of the Booking model
    '''
    # Unique ID for the booking
    # -> primary key for the model
    id = db.Column(
        db.Integer, primary_key=True)
    # Date the booking was made
    date = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # Date the listing reservation will begin
    start = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # Date the listing reservation will end
    end = db.Column(
        db.DateTime(timezone=True), nullable=False)
    # The amount the user paid
    price = db.Column(
        db.Float, nullable=False)
    # The user ID of the user renting the property
    user_id = db.Column(
        db.Integer, nullable=False)
    # The ID of the listing being booked
    listing_id = db.Column(
        db.Integer, nullable=False)

    def __repr__(self):
        return '<Booking %r>' % self.id


class Review(db.Model):
    '''
    Description: Definition of the Review model
    '''
    # Unique ID of review
    # -> Primary key of the table
    id = db.Column(db.Integer, primary_key=True)
    # ID of the user that made the review
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    # Listing ID that the review belong to
    listing_id = db.Column(db.Integer, unique=False, nullable=False)
    # Review message
    review_text = db.Column(db.String(1000), unique=False, nullable=False)
    # Date of review creation
    date = db.Column(
        db.DateTime(timezone=True), unique=False, nullable=False)

    def __repr__(self):
        return '<Review %r>' % self.review_id


# create all tables
db.create_all()


# Put Assignment 2 functions here

def create_listing(title, description, price, date, email):
    # R4-1: Make sure title does not start with or end with a space
    if title.startswith(' '):
        print("ERROR: leading space in title.")
        return False
    if title.endswith(' '):
        print("ERROR: trailing space in title.")
        return False

    # R4-1: Make sure title is alphanumeric with spaces
    if all(x.isalnum() or x.isspace() for x in title) is False:
        print("ERROR: Special characters in listing title.")
        return False

    # R4-2: Make sure the title is 80 characters max
    if len(title) > 80:
        print("ERROR: Listing title longer than 80 chars.")
        return False

    # R4-3: Make sure the description is between 20 and 2000 characters
    if len(description) < 20 or len(description) > 2000:
        print("ERROR: Description should be 20-2000 characters")
        return False

    # R4-4: Make sure the description is longer than the title
    if len(description) <= len(title):
        print("ERROR: Description must be longer than title.")
        return False

    # R4-5: Make sure the price is in the range [10-10000]
    if price < 10:
        print("ERROR: Price too low")
        return False
    if price > 10000:
        print("ERROR: Price too high")
        return False

    # Put date in datetime format (set time to arbitrary 12pm)
    date += " 12:00:00"
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    # Define first and last possible day for last modified date
    first = datetime.strptime("2021-01-02 23:59:59", '%Y-%m-%d %H:%M:%S')
    last = datetime.strptime("2025-01-02 00:00:00", '%Y-%m-%d %H:%M:%S')

    # R4-6: Last modified date must be between 2021-01-02 and 2025-01-02
    if first > date or date > last:
        print("ERROR: Invalid last modified date")
        return False

    # R4-7: User email cannot be empty and must be in the database
    if email == None or email == "":
        print("ERROR: User email cannot be empty")
        return False
    # check if the email is registered to a user:
    user_email = User.query.filter_by(email=email).all()
    if len(user_email) == 0:
        print("ERROR: Email not registered")
        return False

    # R4-8: The listing title must be unique
    listing_title = Listing.query.filter_by(name=title).all()
    if len(listing_title) > 0:
        print("ERROR: Listing title already used")
        return False


    # create a new listing

    # get the largest id. Each id will be the previous largest id + 1
    id = 0
    listing_id = db.session.query(Listing.id)
    # search for the largest id value that was returned from the query
    for i in listing_id:
        cur_id = i[0]
        # If the current id is larger than id, set id to the current id
        if id < cur_id:
            id = cur_id
    
    # Add 1 to id
    id+=1

    # Get the user_id that corresponds to the user_email
    query = User.query.filter_by(email=email).first()
    user_id = query.id

    listing = Listing(id=id, name=title, description=description, price=price, date=date, user_email=email, user_id=user_id)
    # add listing to the current database session
    db.session.add(listing)
    # actually save the user object
    db.session.commit()

    return True

def create_user():
    user = User(id=0, email="test0@test.com", username="example", password="passw0rd!", billing_address="123 Test Street", postal_code="A0A0A0", account_balance=1000)
    db.session.add(user)
    db.session.commit()
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

    # Password of the user's account -> doesn't have to be unique
    password = db.Column(db.String(120), unique=False, nullable=False)

    # Username of the user's account -> must be unique to identify each account
    username = db.Column(db.String(120), unique=True, nullable=False)

    # Billing Address
    billing_address = db.Column(db.String(120), unique=False, nullable=False)

    # Postal Code
    postal_code = db.Column(db.String(120), unique=False, nullable=False)

    # Account Balance
    balance = db.Column(db.Float, unique=False, nullable=False)

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
    address = db.Column(db.String(120), unique=True, nullable=True)
    # Daily price of the listing
    price = db.Column(db.Float, unique=False, nullable=False)
    # Listing description
    description = db.Column(db.String(2000), unique=False, nullable=False)
    # Unique ID of the owner
    # -> primary key of owner
    owner_id = db.Column(db.Integer, primary_key=True)
    # Last Mofified Date
    last_modified_date = db.Column(db.DateTime, unique=False, nullable=False)

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
def update_listing(id, name, description, price, email):
    '''
    Description: Update Listing
        Parameters:
            id (Integer): Listing ID
            name (String): Listing Name
            price (String): Listing Price
            description (String): Listing Description
            email (String): User Email
        Returns:
            True if product update succeeded otherwise False
    '''
    # Check if name contains only alphanumeric chars and spaces
    if not name.replace(" ", "").isalnum():
        return
    # Check if name starts or ends with a space
    if (name.startswith(' ') or
            name.endswith(' ')):
        return
    # Check the length of name
    if len(name) > 80:
        return
    # Check the length of description
    if (len(description) > 2000 or
            len(description) < 20):
        return
    # Check if the description is longer than the name
    if len(description) <= len(name):
        return
    # Check if the price is in the correct range
    if not (price in range(10, 10001)):
        return
    # Check if price has increased
    price_list = Listing.query.filter_by(price=price).all()
    for p in price_list:
        if price < p:
            return
    # Owner email cannot be empty
    if email is None or email == "":
        return
    # Check if email is a valid email address
    if len(User.query.filter_by(email=email).all()) == 0:
        return
    # Check if user created a listing with a name that already 
    # exists
    if name in Listing.query.filter_by(name=name).all():
        return
    # Update date when update operation is successful
    date = datetime.now()
    # Check last_modified_date must be after 2021-01-02 and before
    # 2025-01-02
    if (date < datetime(2021, 1, 2) or date > datetime(2025, 1, 2)):
        return
    # Get the user_id that corresponds to the user_email
    query = User.query.filter_by(email=email).first()
    user_id = query.owner_id
    # Update listing
    listing = Listing(id=id, name=name, price=price, description=description,
                      owner_id=user_id, last_modified_date=date)
    db.session.update(listing)
    db.session.commit()
    return True

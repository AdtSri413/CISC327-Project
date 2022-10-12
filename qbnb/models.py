from qbnb import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# external library used to validate user email address
from email_validator import validate_email, EmailNotValidError
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
def register(username, email, password):
    '''
    Check register parameters
        Parameters:
            username (string): user username
            email (string): user email
            password (string): user password
        Returns:
            User object if register succeeds, otherwise None
    '''
    if not verify_username(username):
        return None
    if not verify_email(email):
        return None
    if not verify_password(password):
        return None
    # getting largest ID in the database so far
    max_id = 0
    results = db.session.query(db.func.max(User.id))
    for row in results:
        if row[0] is not None:
            max_id = row[0]
    # R1-8: Billing address is empty at registration
    # R1-9: Postal code is empty at registration
    # R1-10: Balance initialised as 100 at registration
    new_user = User(username=username, email=email, password=password, 
                    billing_address="", postal_code="", balance=100, 
                    id=(max_id + 1))
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        # re-activates session if error detected while committing
        db.session.rollback()
    return new_user
    

def verify_username(username):
    '''
    Helper function to validate username
        Parameters:
            username (string): user username
        Returns:
            True if username is valid, otherwise False
    '''
    # R1-5: Cannot be empty
    if username is None or username == "":
        return False
    # R1-5: Alphanumeric only
    if not username.replace(" ", "").isalnum():
        return False
    # R1-5: Space allowed only if not prefix or suffix
    if username[0] == " " or username[-1] == " ":
        return False
    # R1-6: Longer than 2 characters and less than 20 characters
    if len(username) <= 2 or len(username) >= 20:
        return False
    return True


def verify_email(email):
    '''
    Helper function to validate email
        Parameters:
            email (string): user email
        Returns:
            True if email is valid, otherwise False
    '''
    # R1-1: Cannot be empty
    if email is None or email == "":
        return False
    # R1-3: Must follow RFC 5322 specifications
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        print(str(e))
        return False
    # R1-7: Cannot be duplicate
    duplicates = User.query.filter_by(email=email).all()
    if len(duplicates) > 0:
        print("duplicates found")
        return False
    return True
    

def verify_password(password):
    '''
    Helper function to validate password
        Parameters:
            password (string): user password
        Returns:
            True if password is valid, otherwise False
    '''
    # R1-1: Cannot be empty.
    if password is None or password == "":
        return False
    
    # R1-4: Minimum length 6
    if len(password) <= 6:
        return False
    
    # R1-4: At least one special character
    special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if not any(c in special_characters for c in password):
        return False
    
    # R1-4: At least one lower case
    if not any(c.islower() for c in password):
        return False
    
    # R1-4: At least one upper case
    if not any(c.isupper() for c in password):
        return False
    
    return True
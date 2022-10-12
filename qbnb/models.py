from qbnb import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
# external library used to validate user email address
from email_validator import validate_email, EmailNotValidError
import re


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
    # initialising max_id as 0 for first ever User in database
    max_id = 0
    # query for maximum value in id column
    results = db.session.query(db.func.max(User.id))
    for row in results:
        if row[0] is not None:
            max_id = row[0]
    # R1-8: Billing address is empty at registration
    # R1-9: Postal code is empty at registration
    # R1-10: Balance initialised as 100 at registration
    new_user = User(username=username, email=email, password=password,
                    billing_address="", postal_code="", balance=100,
                    id=(max_id + 1))  # increments max_id by 1 for uniqueness
    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        # re-activates session if error detected while committing
        db.session.rollback()
    return new_user


def login(email, password):
    '''
    Check login parameters
        Parameters:
            email (string):    user email
            password (string): user password
        Returns:
            The user object if login succeeded otherwise None
    '''

    # Email and password should meet the required specification
    if not verify_email_login(email):
        return None

    if not verify_password(password):
        return None

    # Check database to see to see if email and password match
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]


def update_user(user_id, username=None, email=None, billing_address=None,
                postal_code=None):
    '''
    Update users data
        Parameters:
            username (string): username
            email (string):    user email
            billing_address (string): user billing address
            postal_code (string): user postal code
        Returns:
            The user object if login succeeded otherwise None
    '''

    toggle = 0

    user = User.query.filter_by(id=user_id).first()

    if username is not None:
        if not verify_username(username):
            return None
        user.username = username

    if email is not None:
        if not verify_email(email):
            return None
        user.email = email

    if billing_address is not None:
        user.billing_address = billing_address

    if postal_code is not None:
        if not postal_code_validation(postal_code):
            return None
        user.postal_code = postal_code

    db.session.commit()

    return user


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
    # queries for all records where email is the same as potential user's
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
    special_characters = " !\"#$%&'()*+,-./:;<=>?@[]^_`{|}~\\"
    if not any(c in special_characters for c in password):
        return False

    # R1-4: At least one lower case
    if not any(c.islower() for c in password):
        return False

    # R1-4: At least one upper case
    if not any(c.isupper() for c in password):
        return False

    return True


def verify_email_login(email):
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

    # Email must exist in database
    valids = User.query.filter_by(email=email).all()
    if len(valids) != 1:
        return False
    return True


def postal_code_validation(postal_code):
    # Supplied postal code should be non-empty
    if postal_code is None or postal_code == "":
        return False

    # supplied postal code should only be alphanumeric
    if not postal_code.isalnum():
        # print(postal_code, postal_code)
        return False

    # supplied postal code should have no special characters
    if not re.match("^[a-zA-Z0-9_]*$", postal_code):
        return False

    # Supplied postal code should be a valid canadian postal code
    cp = re.compile("[ABCEGHJKLMNPRSTVXY]"
                    "[0-9]"
                    "[ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]"
                    )
    m = re.match(cp, postal_code)
    print(postal_code, m)
    if m:
        return True

    return False


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
    if email is None or email == "":
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
    id += 1

    # Get the user_id that corresponds to the user_email
    query = User.query.filter_by(email=email).first()
    user_id = query.id

    listing = Listing(id=id, name=title, description=description,
                      price=price, last_modified_date=date,
                      owner_id=user_id)
    # add listing to the current database session
    db.session.add(listing)
    # actually save the user object
    db.session.commit()

    return True


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

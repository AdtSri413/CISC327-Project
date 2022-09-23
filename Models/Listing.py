'''
Description: Defines the Listing model
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


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

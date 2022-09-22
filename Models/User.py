'''
Description: Defines the User model
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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

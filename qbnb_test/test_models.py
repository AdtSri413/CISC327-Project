'''
Test code for qbnb/models.py (Assignment 1 models and assignment 2 functions)
'''

from qbnb.models import *

def app_context():
    with app.app_context():
        yield

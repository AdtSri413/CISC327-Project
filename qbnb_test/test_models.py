'''
Test code for qbnb/models.py (Assignment 1 models and assignment 2 functions)
'''

from qbnb.models import register, login


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
      (will be tested after the previous test, so we already have u0, 
      in database)
    '''

    register(username="user 0", email="test0@test.com", password="Test123?")

    user = login('test0@test.com', 'Test123?')
    assert user is not None
    assert user.username == 'user 0'

    # Incorrect password
    user = login('test0@test.com', '1234567')
    assert user is None

    # Incorrect email
    user = login('test1@test.com', '123456')
    assert user is None


def test_r2_2_login():
    '''
    Testing R2-2: The login function should check if the supplied inputs 
    meet the same email/password requirements as above, before checking the database.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    # Email should not be empty
    user = login("", "Test123?")
    assert user is None
    user = login(None, "Test123?")
    assert user is None

    # Email has to follow addr-spec defined in RFC 5322
    user = login("test1.@test.com", "Test123?")
    assert user is None

    # Password does not meet minimum length of 6
    user = login('test0@test.com', 'Ab@12')
    assert user is None

    # Password does not have at least 1 upper case
    user = login('test0@test.com', 'ab@123')
    assert user is None

    # Password does not have at least 1 lower case
    user = login('test0@test.com', 'AB@123')
    assert user is None

    # Password does not have at least 1 special case
    user = login('test0@test.com', 'Abc123')
    assert user is None

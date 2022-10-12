'''
Test code for qbnb/models.py (Assignment 1 models and assignment 2 functions)
'''

from qbnb.models import register, create_listing, login, update_user


# R1-1: Email cannot be empty. password cannot be empty.
def test_r1_1_register():
    assert register(username="user 0", email="test0@test.com",
                    password="Test123?") is not None
    assert register(username="user 1", email=None,
                    password="Test123?") is None
    assert register(username="user 1", email="test1@test.com",
                    password=None) is None
    assert register(username="user 1", email="",
                    password="Test123?") is None
    assert register(username="user 1", email="test1@test.com",
                    password="") is None


# R1-2: A user is uniquely identified by
# his/her user id - automatically generated
def test_r1_2_register():
    # not sure how to check uniqueness in python
    user1 = register(username="user 10", email="test10@test.com",
                     password="Test123?")
    user2 = register(username="user 11", email="test11@test.com",
                     password="Test123?")
    assert user1.id != user2.id


# R1-3: The email has to follow addr-spec defined in
# RFC 5322 (see https://en.wikipedia.org/wiki/Email_address
# for a human-friendly explanation).
# You can use external libraries/imports.
def test_r1_3_register():
    assert register(username="user 1", email="test1@test.com",
                    password="Test123?") is not None
    assert register(username="user 1", email="test1.@test.com",
                    password="Test123?") is None


# R1-4: Password has to meet the required complexity:
# minimum length 6, at least one upper case,
# at least one lower case, and at least one special character.
def test_r1_4_register():
    assert register(username="user 2", email="test2@test.com",
                    password="Test123?") is not None
    assert register(username="user 3", email="test3@test.com",
                    password="Tt1?") is None
    assert register(username="user 3", email="test3@test.com",
                    password="test123?") is None
    assert register(username="user 3", email="test3@test.com",
                    password="TEST123?") is None
    assert register(username="user 3", email="test3@test.com",
                    password="Test123") is None


# R1-5: User name has to be non-empty, alphanumeric-only,
# and space allowed only if it is not as the prefix or suffix.
def test_r1_5_register():
    assert register(username="user 4", email="test4@test.com",
                    password="Test123?") is not None
    assert register(username=None, email="test5@test.com",
                    password="Test123?") is None
    assert register(username="user 5!", email="test5@test.com",
                    password="Test123?") is None
    assert register(username=" user 5", email="test5@test.com",
                    password="Test123?") is None
    assert register(username="user 5 ", email="test5@test.com",
                    password="Test123?") is None


# R1-6: User name has to be longer than 2 characters and
# less than 20 characters.
def test_r1_6_register():
    assert register(username="user 5", email="test5@test.com",
                    password="Test123?") is not None
    assert register(username="u6", email="test6@test.com",
                    password="Test123?") is None
    assert register(username="user 6 user 6 user 6 user 6",
                    email="test6@test.com", password="Test123?") is None


# R1-7: If the email has been used, the operation failed.
def test_r1_7_register():
    assert register(username="user 6", email="test6@test.com",
                    password="Test123?") is not None
    assert register(username="user 7", email="test6@test.com",
                    password="Test123?") is None


# R1-8: Shipping address is empty at the time of registration.
def test_r1_8_register():
    user = register(username="user 7", email="test7@test.com",
                    password="Test123?")
    assert user.billing_address == ""


# R1-9: Postal code is empty at the time of registration.
def test_r1_9_register():
    user = register(username="user 8", email="test8@test.com",
                    password="Test123?")
    assert user.postal_code == ""


# R1-10: Balance should be initialized as 100 at the time
#  of registration. (free $100 dollar signup bonus).
def test_r1_10_register():
    user = register(username="user 9", email="test9@test.com",
                    password="Test123?")
    assert user.balance == 100


def test_r4_1_create_listing():
    '''
    Testing R4-1: If the title is not alphanumeric only or begins/ends
    with a space, the operation failed
    '''

    assert create_listing(
        'Ex title R4 1 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        ' Ex title R4 1 2', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is False

    assert create_listing(
        'Ex title R4 1 3 ', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is False

    assert create_listing(
        'Ex title R4-1 4', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is False


def test_r4_2_create_listing():
    '''
    Testing R4-2: If the title is longer than 80 characters, the operation 
    failed
    '''

    assert create_listing(
        'Ex title R4 2 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        '4 bedroom 4 bathroom house on the water comes with outdoor \
            heated pool',
        'beautiful large house on the water. perfect for your vacation needs. \
            Enjoy a gorgeous outdoor heated pool during your stay.',
        1000,
        '2022-10-05',
        'test0@test.com') is False


def test_r4_3_create_listing():
    '''
    Testing R4-3: If the description is shorter than 20 characters or longer
    than 2000 characters, the operation failed
    '''

    assert create_listing(
        'Ex title R4 3 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 3 2', 'Ex description',
        1000, '2022-10-05', 'test0@test.com') is False

    assert create_listing(
        'Ex title R4 3 3', 'x' * 2001, 1000, '2022-10-05', 'test0@test.com') \
        is False


def test_r4_4_create_listing():
    '''
    Testing R4-4: If the description is shorter than the title, the 
    operation failed
    '''

    assert create_listing(
        'Ex title R4 4 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 4 2', 'Ex desc',
        1000, '2022-10-05', 'test0@test.com') is False


def test_r4_5_create_listing():
    '''
    Testing R4-5: If the price is not between 10 and 10000, the operation 
    failed
    '''

    assert create_listing(
        'Ex title R4 5 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 5 2', 'Ex description of listing',
        9, '2022-10-05', 'test0@test.com') is False

    assert create_listing(
        'Ex title R4 5 3', 'Ex description of listing',
        10001, '2022-10-05', 'test0@test.com') is False


def test_r4_6_create_listing():
    '''
    Testing R4-6: If the last modified date is not after 2021-01-02 and before 
    2025-01-02, the operation failed
    '''

    assert create_listing(
        'Ex title R4 6 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 6 2', 'Ex description of listing',
        1000, '2021-01-01', 'test0@test.com') is False

    assert create_listing(
        'Ex title R4 6 3', 'Ex description of listing',
        1000, '2025-01-03', 'test0@test.com') is False


def test_r4_7_create_listing():
    '''
    Testing R4-7: If the user email is empty or does not exist in the 
    User database, the operation failed
    '''

    assert create_listing(
        'Ex title R4 7 1', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 7 2', 'Ex description of listing',
        1000, '2022-10-05', None) is False

    assert create_listing(
        'Ex title R4 7 3', 'Ex description of listing',
        1000, '2022-10-05', '') is False

    assert create_listing(
        'Ex title R4 7 4', 'Ex description of listing',
        1000, '2022-10-05', 'nottest0@test.com') is False


def test_r4_8_create_listing():
    '''
    Testing R4-8: If the listing title already exists in the database, 
    the operation failed
    '''
    assert create_listing(
        'Ex title R4 8', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 8', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is False


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
    meet the same email/password requirements as above, before checking 
    the database.
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


def test_r3_1_update_user():
    '''
    Testing R3-1: The update_user function is able to update user's 
    user name, user email, billing address and postal code
    '''
    user = update_user(user_id=1, username="Tommy", email="tommy@gmail.com",
                       billing_address="45 Union Street", postal_code="K7L2N8")
    assert user is not None
    assert user.username == "Tommy"
    assert user.email == "tommy@gmail.com"
    assert user.billing_address == "45 Union Street"
    assert user.postal_code == "K7L2N8"


def test_r3_2_update_user():
    '''
    Testing R3-2: The update_user function should check if the 
    supplied postal code non-empty, alphanumeric-only and has 
    no special characters, before checking the database.
    '''
    # Supplied postal code should be non-empty
    user = update_user(user_id=1, postal_code="")
    assert user is None

    # Supplied postal code should be alphanumeric only
    user = update_user(user_id=1, postal_code="K7L 2N8")
    assert user is None

    # Supplied postal code sould have no special characters
    user = update_user(user_id=1, postal_code="K7L2N@")
    assert user is None


def test_r3_3_update_user():
    '''
    Testing R3-3: The update_user function should check if the supplied postal 
    code is a valid canadian postal code, before checking the database
    '''

    # Supplied postal code should be a valid canadian postal code
    # (leading Z is not allowed)
    user = update_user(user_id=1, postal_code="Z7L2N8")
    assert user is None


def test_r3_4_update_user():
    '''
    Testing R3-4: The update_user function should check if the supplied 
    username follows the above requirement, before checking the database

    '''

    # Supplied username should be non-empty
    user = update_user(user_id=1, postal_code="")
    assert user is None

    # Supplied username should be alphanumeric-only
    user = update_user(user_id=1, postal_code="K7L 2N8")
    assert user is None

    # Supplied username should have space allowed only if it is not
    # as the prefix or suffix
    user = update_user(user_id=1, username=" K7L2N8")
    assert user is None

    # Supplied username should be longer than 2 characters
    user = update_user(user_id=1, username="a")
    assert user is None

    # Supplied username should be less than 20 characters
    user = update_user(user_id=1, username="abcdefghijklmnopqrstu")
    assert user is None

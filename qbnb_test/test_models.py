'''
Test code for qbnb/models.py (Assignment 1 models and assignment 2
functions)
'''

from qbnb.models import update_listing


def test_r5_1_update_listing():
    '''
    Testing R5-1: Can update all attributes of a listing except the
    owner_id and the last_modified_date
    '''

    assert update_listing(
        'Ex title R5 1 1', 'Ex description of listing', 1000, 
        'test@test.com') is True


def test_r5_2_update_listing():
    '''
    Testing RD-2: The price can only increase or stay the same
    '''

    assert update_listing(
        'Listing 1', 'Ex description of listing', 1000,
        'test@test.com') is True
    assert update_listing(
        'Listing 1', 'Ex description of listing', 900,
        'test@test.com') is False
    assert update_listing(
        'Listing 1', 'Ex description of listing', 1100,
        'test@test.com') is True


def test_r5_4_1_update_listing():
    '''
    Testing R5-4-1: If the title is not alphanumeric only or 
    begins/ends with a space, the operation failed
    '''

    assert update_listing(
        'Ex title R5 4 1 1', 'Ex description of listing', 1000, 
        'test0@test.com') is True

    assert update_listing(
        ' Ex title R5 4 1 2', 'Ex description of listing', 1000,
        'test0@test.com') is False
    
    assert update_listing(
        'Ex title R5 4 1 3 ', 'Ex description of listing', 1000,
        'test0@test.com') is False

    assert update_listing(
        'Ex title R5 4 1 4', 'Ex description of listing', 1000,
        'test0@test.com') is False


def test_r5_4_2_update_listing():
    '''
    Testing R5-4-2: If the title is longer than 80 characters, the
    operation failed
    '''

    assert update_listing(
        'Ex title R5 4 2 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        '4 bedroom 4 bathroom house on the water comes with outdoor heated \
        pool', 'beautiful large house on the water. perfect for your \
        vacation needs. Enjoy a gorgeous outdoor heated pool during your \
        stay.', 1000, 'test0@test.com') is False


def test_r5_4_3_update_listing():
    '''
    Testing R5-4-3: If the description is shorter than 20 characters or
    longer than 2000 characters, the operation failed
    '''

    assert update_listing(
        'Ex title R5 4 3 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        'Ex title R5 4 3 2', 'Ex description', 1000, 'test0@test.com') \
        is False

    assert update_listing(
        'Ex title R5 4 3 3', 'x' * 2001, 1000, 'test0@test.com') is False


def test_r5_4_4_update_listing():
    '''
    Testing R5-4-4: If the description is shorter than the title, the 
    operation failed
    '''

    assert update_listing(
        'Ex title R5 4 4 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        'Ex title R5 4 4 2', 'Ex desc', 1000, 'test0@test.com') is False


def test_r5_4_5_update_listing():
    '''
    Testing R5-4-5: If the price is not between 10 and 10000,
    the operation failed
    '''

    assert update_listing(
        'Ex title R5 4 5 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        'Ex title R5 4 5 2', 'Ex description of listing', 9,
        'test0@test.com') is False

    assert update_listing(
        'Ex title R5 5 3', 'Ex description of listing', 10001,
        'test0@test.com') is False


def test_r5_4_6_update_listing():
    '''
    Testing R5-4-6: If the user email is empty or does not exist in the 
    User database, the operation failed
    '''

    assert update_listing(
        'Ex title R5 4 6 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        'Ex title R5 4 6 2', 'Ex description of listing', 1000, None) \
        is False

    assert update_listing(
        'Ex title R5 4 7 3', 'Ex description of listing', 1000, '') is False    

    assert update_listing(
        'Ex title R5 4 7 4', 'Ex description of listing', 1000,
        'nottest0@test.com') is False


def test_r5_4_7_update_listing():
    '''
    Testing R5-4-8: If the listing title already exists in the database, 
    the operation failed
    '''
    assert update_listing(
        'Ex title R5 4 8 1', 'Ex description of listing', 1000,
        'test0@test.com') is True

    assert update_listing(
        'Ex title R5 4 8 2', 'Ex description of listing', 1000,
        'test0@test.com') is False

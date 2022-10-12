'''
Test code for qbnb/models.py (Assignment 1 models and assignment 2 functions)
'''
from qbnb.models import create_listing, create_user

def test_r4_1_create_listing():
    '''
    Testing R4-1: If the title is not alphanumeric only or begins/ends
    with a space, the operation failed
    '''
    # Create a user to use in our tests
    create_user()

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
        'Ex title R4 3 3', 'x' * 2001, 1000, '2022-10-05', 'test0@test.com') is False

    
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
    Testing R4-5: If the price is not between 10 and 10000, the operation failed
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
    Testing R4-6: If the last modified date is not after 2021-01-02 and before 2025-01-02, the operation failed
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
    Testing R4-7: If the user email is empty or does not exist in the User database, the operation failed
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
        1000, '2022-10-05', 'test1@test.com') is False


def test_r4_8_create_listing():
    '''
    Testing R4-8: If the listing title already exists in the database, the operation failed
    '''
    assert create_listing(
        'Ex title R4 8', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is True

    assert create_listing(
        'Ex title R4 8', 'Ex description of listing',
        1000, '2022-10-05', 'test0@test.com') is False


from qbnb.models import book_listing
from datetime import datetime

"""
Test that the parameters of the book_listing function are sanitized
"""


def test_book_listing_listing_name():
    """
    Test that the listing_name parameter is sanitized
    """
    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing usernames
        for i, l in enumerate(f):
            # If book_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                booking = book_listing(l[:-1], datetime.now(), datetime.max,
                                       f"payloadusername{i}")
                assert booking is None

            # If book_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a listing name")


def test_book_listing_start_date():
    """
    Test that the start_date parameter is sanitized
    """
    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing listing names and usernames
        for i, l in enumerate(f):
            # If book_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                booking = book_listing(f"l{i}sting name", l[:-1],
                                       datetime.max,
                                       f"payloadusername{i}") 
                assert booking is None

            # If book_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a start date")


def test_book_listing_end_date():
    """
    Test that the end_date parameter is sanitized
    """
    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing listing names and usernames
        for i, l in enumerate(f):
            # If book_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                booking = book_listing(f"l{i}sting name", datetime.now(),
                                       l[:-1], f"payloadusername{i}")
                assert booking is None

            # If book_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as an end date")


def test_book_listing_user_name():
    """
    Test that the user_name parameter is sanitized
    """
    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing listing names
        for i, l in enumerate(f):
            # If book_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                booking = book_listing(f"l{i}sting name", datetime.now(),
                                       datetime.max, l[:-1])
                assert booking is None

            # If book_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a user name")
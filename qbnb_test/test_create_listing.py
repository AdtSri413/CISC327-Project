from qbnb.models import create_listing
from datetime import datetime


def test_create_listing_title():

    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing emails
        for i, l in enumerate(f):
            # If create_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                listing = create_listing(l[:-1],
                                         "Example property description", 11,
                                         datetime.now(),
                                         f"payloadusername{i}@gmail.com")
                assert listing is None

            # If create_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a title")


def test_create_listing_description():

    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing titles and emails
        for i, l in enumerate(f):
            # If create_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                listing = create_listing(f"t{i}tle", l[:-1], 11,
                                         datetime.now(),
                                         f"payloadusername{i}@gmail.com") 
                assert listing is None

            # If create_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a description")


def test_create_listing_price():

    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing titles and emails
        for i, l in enumerate(f):
            # If create_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                listing = create_listing(f"t{i}tle",
                                         "Example property description",
                                         l[:-1], datetime.now(),
                                         f"payloadusername{i}@gmail.com") 
                assert listing is None

            # If create_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a price")


def test_create_listing_date():

    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing titles and emails
        for i, l in enumerate(f):
            # If create_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                listing = create_listing(f"t{i}tle",
                                         "Example property description", 11,
                                         l[:-1],
                                         f"payloadusername{i}@gmail.com") 
                assert listing is None

            # If create_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as a date")


def test_create_listing_email():

    # Read sql injections
    with open("qbnb_test/sql_injection.txt", "r") as f:
        # Read each line in file
        # Counter to ensure we are not reusing titles
        for i, l in enumerate(f):
            # If create_listing returns None, it means the payload did not work
            try:
                # Use l[:-1] to remove \n at the end of the payload
                listing = create_listing(f"t{i}tle",
                                         "Example property description", 11,
                                         datetime.now(), l[:-1]) 
                assert listing is None

            # If create_listing does not return None, it means the sql
            # injection went through
            except (AssertionError):
                print(f"Parameter {l} works as an email")
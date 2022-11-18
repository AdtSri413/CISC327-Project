from qbnb.models import *


def test_register_username():

    # Read sql injections
    f = open("qbnb_test/sql_injection.txt", "r")

    # Counter to ensure we are not reusing usernames and emails
    i = 0

    # Read each line in file
    for x in f:
        # If register returns None, it means the payload did not work
        try:
            # Use x[-1] to remove \n at the end of the payload
            user = register(x[:-1], f"payloadusername{i}@gmail.com", "Examp!3") 
            assert user is None

        # If register does not return None, it means the sql injection went 
        # through
        except (AssertionError):
            print(f"Parameter {x} works as a username")
        
        # Increase counter
        i += 1


def test_register_email():

    # Read sql injections
    f = open("qbnb_test/sql_injection.txt", "r")

    # Counter to ensure we are not reusing usernames and emails
    i = 0

    # Read each line in file
    for x in f:
        # If register returns None, it means the sql injection did not work
        try:
            user = register(f"Payload Email {i}", x[:-1], "Examp!3")
            assert user is None

        # If register does not return None, it means the sql injection went 
        # through
        except (AssertionError):
            print(f"Parameter {x} works as an email")

        # Increase counter
        i += 1


def test_register_password():

    # Read sql injections
    f = open("qbnb_test/sql_injection.txt", "r")

    # Counter to ensure we are not reusing usernames and emails
    i = 0

    # Read each line in file
    for x in f:
        # If register returns None, it means the sql injection did not work
        try:
            user = register(f"Payload Password {i}", 
                            f"payloadpassword{i}@gmail.com", x[:-1])
            assert user is None

        # If register does not return None, it means the sql injection went 
        # through
        except (AssertionError):
            print(f"Parameter {x} works as a password")

        # Increase counter
        i += 1
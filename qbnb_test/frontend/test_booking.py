from seleniumbase import BaseCase

from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models import User


class FrontEndBookingTest(BaseCase):
    '''
    Uses EXHAUSTIVE OUTPUT TESTING as white-box testing methodology
        - Successful booking
        - Failed booking -> not allowed to book own listing
        - Failed booking -> overlapping dates
        - Failed booking -> insufficient balance
    '''
    def test_booking_1(self, *_):
        '''
        Test should produce successful booking message
        '''
        # register as agent
        self.open(base_url + '/register')
        self.type("#email", "agent001@test.com")
        self.type("#name", "Agent001")
        self.type("#password", "Agent001!")
        self.type("#password2", "Agent001!")
        self.click('input[type="submit"]')
        # login as agent
        self.open(base_url + '/login')
        self.type("#email", "agent001@test.com")
        self.type("#password", "Agent001!")
        self.click('input[type="submit"]')
        # create booking
        # logout
        # register as customer
        self.open(base_url + '/register')
        self.type("#email", "cust001@test.com")
        self.type("#name", "Cust001")
        self.type("#password", "Cust001!")
        self.type("#password2", "Cust001!")
        self.click('input[type="submit"]')
        # login as customer
        self.open(base_url + '/login')
        self.type("#email", "cust001@test.com")
        self.type("#password", "Cust001!")
        self.click('input[type="submit"]')
        # reserve booking -> should display successful booking message


    def test_booking_2(self, *_):
        '''
        Test should produce "cannot book own listing" message
        '''
        # register as agent
        self.open(base_url + '/register')
        self.type("#email", "agent002@test.com")
        self.type("#name", "Agent002")
        self.type("#password", "Agent002!")
        self.type("#password2", "Agent002!")
        self.click('input[type="submit"]')
        # login as agent
        self.open(base_url + '/login')
        self.type("#email", "agent002@test.com")
        self.type("#password", "Agent002!")
        self.click('input[type="submit"]')
        # create booking
        # reserve booking as agent -> booking should fail


    def test_booking_3(self, *_):
        '''
        Test should produce "already booked on these dates" message
        '''
        # register as agent
        self.open(base_url + '/register')
        self.type("#email", "agent003@test.com")
        self.type("#name", "Agent003")
        self.type("#password", "Agent003!")
        self.type("#password2", "Agent003!")
        self.click('input[type="submit"]')
        # login as agent
        self.open(base_url + '/login')
        self.type("#email", "agent003@test.com")
        self.type("#password", "Agent003!")
        self.click('input[type="submit"]')
        # create booking
        # register as customer 1
        self.open(base_url + '/register')
        self.type("#email", "cust002@test.com")
        self.type("#name", "Cust002")
        self.type("#password", "Cust002!")
        self.type("#password2", "Cust002!")
        self.click('input[type="submit"]')
        # login as customer 1
        self.open(base_url + '/login')
        self.type("#email", "cust002@test.com")
        self.type("#password", "Cust002!")
        self.click('input[type="submit"]')
        # reserve booking -> booking should succeed
        # register as customer 2
        self.open(base_url + '/register')
        self.type("#email", "cust003@test.com")
        self.type("#name", "Cust003")
        self.type("#password", "Cust003!")
        self.type("#password2", "Cust003!")
        self.click('input[type="submit"]')
        # login as customer 2
        self.open(base_url + '/login')
        self.type("#email", "cust003@test.com")
        self.type("#password", "Cust003!")
        self.click('input[type="submit"]')
        # reserve booking in same date range as above -> booking should fail


    def test_booking_4(self, *_):
        '''
        Test should produce "insufficient balance" message
        '''
        # register as agent
        self.open(base_url + '/register')
        self.type("#email", "agent002@test.com")
        self.type("#name", "Agent002")
        self.type("#password", "Agent002!")
        self.type("#password2", "Agent002!")
        self.click('input[type="submit"]')
        # login as agent
        self.open(base_url + '/login')
        self.type("#email", "agent002@test.com")
        self.type("#password", "Agent002!")
        self.click('input[type="submit"]')
        # create booking with very high cost
        # register as customer
        self.open(base_url + '/register')
        self.type("#email", "cust004@test.com")
        self.type("#name", "Cust004")
        self.type("#password", "Cust004!")
        self.type("#password2", "Cust004!")
        self.click('input[type="submit"]')
        # login as customer
        self.open(base_url + '/login')
        self.type("#email", "cust004@test.com")
        self.type("#password", "Cust004!")
        self.click('input[type="submit"]')
        # reserve high cost booking -> booking should fail
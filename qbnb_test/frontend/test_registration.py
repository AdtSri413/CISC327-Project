from seleniumbase import BaseCase

from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models import User

"""
This file defines all integration tests for the frontend homepage.
"""

class FrontEndRegistrationTest(BaseCase):
    '''
    Utilises BOUNDARY TESTING to test the limits of registration details.
    '''
    def test_password_length_1(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and name
        self.type("#email", "test000@test.com")
        self.type("#name", "test000")
        # invalid password (below minimum requirement of 6 characters)
        self.type("#password", "Te0!")
        self.type("#password2", "Te0!")
        # submit registration form
        self.click('input[type="submit"]')
        # test should fail
        # should display registration page with failure message
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
    def test_password_length_2(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and name
        self.type("#email", "test001@test.com")
        self.type("#name", "test001")
        # valid password (exactly minimum requirement of 6 characters)
        self.type("#password", "Test1!")
        self.type("#password2", "Test1!")
        # submit registration form
        self.click('input[type="submit"]')
        # test should pass
        # should display home page with welcome message
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, test001!", "#welcome-header")
    def test_username_length_1(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and password
        self.type("#email", "test002@test.com")
        self.type("#password", "Test2!")
        self.type("#password2", "Test2!")
        # invalid username (exactly 2 characters)
        self.type("#name", "t2")
        # submit registration form
        self.click('input[type="submit"]')
        # test should fail
        # should display register page with failure message
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
    def test_username_length_2(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and password
        self.type("#email", "test002@test.com")
        self.type("#password", "Test2!")
        self.type("#password2", "Test2!")
        # invalid username (exactly 20 characters)
        self.type("#name", "12345678901234567890")
        # submit registration form
        self.click('input[type="submit"]')
        # test should fail
        # should display register page with failure message
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
    def test_username_length_3(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and password
        self.type("#email", "test002@test.com")
        self.type("#password", "Test2!")
        self.type("#password2", "Test2!")
        # valid username (just more than 2 characters)
        self.type("#name", "t02")
        # submit registration form
        self.click('input[type="submit"]')
        # test should pass
        # should display home page with welcome message
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, t02", "#welcome-header")
    def test_username_length_4(self, *_):
        # open registration page
        self.open(base_url + '/register')
        # valid email and password
        self.type("#email", "test003@test.com")
        self.type("#password", "Test3!")
        self.type("#password2", "Test3!")
        # valid username (just below 20 characters)
        self.type("#name", "1234567890123456789")
        # submit registration form
        self.click('input[type="submit"]')
        # test should pass
        # should display home page with welcome message
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, 1234567890123456789", "#welcome-header")
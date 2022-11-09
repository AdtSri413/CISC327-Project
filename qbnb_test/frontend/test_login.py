from seleniumbase import BaseCase

from qbnb_test.conftest import base_url
from unittest.mock import patch
from qbnb.models import User

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndLoginPageTest(BaseCase):
    '''
    Utilises REQUIREMENTS PARTITIONING TESTING to test login functionality.
    '''
    def test_login_1(self, *_):
        # Setup: User must first be registered
        self.open(base_url + '/register')
        self.type("#email", "test004@test.com")
        self.type("#name", "test004")
        self.type("#password", "Test004!")
        self.type("#password2", "Test004!")
        self.click('input[type="submit"]')
        # Logout from home page
        self.click_link("logout")
        # R1: User should be able to open login page
        self.open(base_url + '/login')
        # R2: User should be able to enter email
        self.type("#email", "test004@test.com")
        # R3: User should be able to enter password
        self.type("#password", "Test004!")
        # click enter button
        self.click('input[type="submit"]')
        # test should pass
        # should redirect to home page with welcome message
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, test004!", "#welcome-header")
    '''
    Uses EXHAUSTIVE OUTPUT COVERAGE to test login functionality.
    There are two possible outputs - success or failure.
    Since success has been covered by test case above, 
    test case below will address failure.
    '''
    def test_login_2(self, *_):
        # Setup: User must first be registered
        self.open(base_url + '/register')
        self.type("#email", "test005@test.com")
        self.type("#name", "test005")
        self.type("#password", "Test005!")
        self.type("#password2", "Test005!")
        self.click('input[type="submit"]')
        # Logout from home page
        self.click_link("logout")
        # Login process starts
        self.open(base_url + '/login')
        # correct email
        self.type("#email", "test005@test.com")
        # wrong password
        self.type("#password", "Wrongpassword5577!")
        # click enter button
        self.click('input[type="submit"]')
        # test should fail
        # should stay on login page and show login failure message
        self.assert_element("#message")
        self.assert_text("login failed", "#message")

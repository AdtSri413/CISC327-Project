from seleniumbase import BaseCase
from qbnb_test.conftest import base_url

"""
This file defines all integration tests for the update user page.
"""


class UpdateUserPageTest(BaseCase):
    """
    Black box: Input testing
    """
    def test_edit_page_nonalphanum_postal(self, *_):
        # Setup: User must first be registered
        self.open(base_url + '/register')
        self.type("#email", "testuser@gmail.com")
        self.type("#name", "User")
        self.type("#password", "Test123?")
        self.type("#password2", "Test123?")
        self.click('input[type="submit"]')

        # open login page
        self.open(base_url + '/')
        # fill email and password
        self.type("#email", "testuser@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update user page
        self.open(base_url + '''/update_user/User''')
        # fill in updated postal_code
        self.type('#postal_code', 'K7L2N@')
        # click submit button
        self.click('input[type="submit"]')
        # test if update user has failed
        self.assert_text("Could not update user")

    def test_edit_page_blank_postal(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "testuser@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update user page
        self.open(base_url + '''/update_user/User''')
        # fill in updated postal_code
        self.type('#postal_code', ' ')
        # click submit button
        self.click('input[type="submit"]')
        # test if update user has failed
        self.assert_text("Could not update user")       

    def test_edit_page_valid_postal(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update user page
        self.open(base_url + '''/update_user/User''')
        # fill in updated postal_code
        self.type('#postal_code', 'K7L 2N8')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Updated user successfully")
from seleniumbase import BaseCase
from qbnb_test.conftest import base_url

"""
This file defines all integration tests for the update user page.
"""


class UpdateUserPageTest(BaseCase):
    """
    Black box: (Input testing postal code)
    """
    def test_edit_page_nonalphanum_postal(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # click update profile page
        self.click_link("Update Profile")
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
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # click update profile page
        self.click_link("Update Profile")
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

        # click update profile page
        self.click_link("Update Profile")
        # fill in updated postal_code
        self.type('#postal_code', 'K7L2N8')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, Tommy", "#welcome-header")

    """
    Black box (Output testing)
    """
    def test_output_fail(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # click update profile page
        self.click_link("Update Profile")
        # fill in invalid name
        self.type('#name', 'a')
        # click submit button
        self.click('input[type="submit"]')
        # test if update user has failed
        self.assert_text("Could not update user")

    def test_output_success(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # click update profile page
        self.click_link("Update Profile")
        # fill in valid name
        self.type('#name', 'Tony')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, Tony", "#welcome-header")

    """
    Functionality coverage test
    """
    
    # One can update all attributes of the listing
    def test_update_all_attributes(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # click update profile page
        self.click_link("Update Profile")
        # fill in name, email, billing_address, postal_code
        self.type('#name', 'Chris')
        self.type('#email', 'chris@hotmail.com')
        self.type('#billing_address', '1234 Main St')
        self.type('#postal_code', 'K7L3N6')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, Chris", "#welcome-header")
        # test if email has been updated
        # log out from home page
        self.click_link("logout")
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "chris@hotmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome, Chris", "#welcome-header")
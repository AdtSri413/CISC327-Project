from seleniumbase import BaseCase
import time

from qbnb_test.conftest import base_url


class UpdateListingPageTest(BaseCase):

    """
    Black box (Input testing price)
    """

    def test_edit_page_price_below(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        self.type('#price', 9)
        self.type('#description', 'Ex description of listing')
        # click submit button
        self.click('input[type="submit"]')
        # test if update listing has failed
        self.assert_text("Could not update listing")

    def test_edit_page_price_at(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        self.type('#price', 1001)
        self.type('#description', 'Ex description of listing')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Here are all of your listings:")

    def test_edit_page_price_above(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        self.type('#price', 10002)
        self.type('#description', 'Ex description of listing')
        # click submit button
        self.click('input[type="submit"]')
        # test if update listing has failed
        self.assert_text("Could not update listing")

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

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', ' illegal $Name')
        self.type('#price', 1)
        self.type('#description', 's')
        # click submit button
        self.click('input[type="submit"]')
        # test if update listing has failed
        self.assert_text("Could not update listing")

    def test_output_success(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        self.type('#price', 1005)
        self.type('#description', 'This is a test description')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Here are all of your listings:")
        self.assert_text('This is a test description')

    """
    Functionality coverage test
    """

    # Price can only increase and not decrease
    def test_price_decrease(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        # Current price is 1005, but we try to decrease it to 1004
        self.type('#price', 1004)
        self.type('#description', 'This is a test description')
        # click submit button
        self.click('input[type="submit"]')
        # test if update listing has failed
        self.assert_text("Could not update listing")

    def test_price_increase(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'Ex title R4 1 1')
        # Current price is 1005, but we try to decrease it to 1004
        self.type('#price', 1006)
        self.type('#description', 'This is a test description')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Here are all of your listings:")

    # One can update all attributes of the listing
    def test_update_all_attributes(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "tommy@gmail.com")
        self.type("#password", "Test123?")
        # click enter button
        self.click('input[type="submit"]')

        # open update listing page
        self.open(base_url + '''/update_listing/Ex title R4 1 1''')
        # fill in name, updated price and description
        self.type('#name', 'New Name Test')
        # Current price is 1005, but we try to decrease it to 1004
        self.type('#price', 1007)
        self.type('#description', 'This is a new test description')
        # click submit button
        self.click('input[type="submit"]')
        # test if user is brought back to home page (sucessful update)
        self.assert_element("#welcome-header")
        self.assert_text("Here are all of your listings:")
        self.assert_text("New Name Test")
        self.assert_text('This is a new test description')

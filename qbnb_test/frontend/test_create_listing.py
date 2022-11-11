from seleniumbase import BaseCase

from qbnb_test.conftest import base_url
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndCreateListingTest(BaseCase):
    '''
    T1: Utilises INPUT PARTITION TESTING to test all possible input partitions
    

    Partitions for the Title box: 
      - P1: Alphanumeric only, correct length (between 1 and 80 characters)
      - P2: not alphanumeric
      - P3: Title is missing
      - P4: longer than 80 characters

    Partitions for the Description Box:
      - P5: Description is between 20 and 2000 characters long, 
            is longer than the title
      - P6: Description is missing
      - P7: Description is less than 20 characters long
      - P8: Description is more than 2000 characters long
      - P9: Description length is less than length of title

    Partitions for the Price Box:
      - P10: Price is correct (between 10 and 10000)
      - P11: Price is missing
      - P12: Price is less than 10
      - P13: Price is more than 10000
    

    T2: Utilises OUTPUT PARTITION TESTING to test all possible output 
        partitions
    
    Output partitions:
      - P1: Listing is created. Website sends user back to homepage 
            and displays a new listing

        NOTE: If exhaustive output coverage testing were used, we 
              would have to test for all the possible listings that 
              could be created, which is not feasible.
      
      - P2: Listing cannot be created because of invalid inputs. 
        Website keeps user on the create listing page and displays an 
        error message.
      
      - P3: There is an invalid input parameter, but the website 
            catches it before attempting to create a listing. Website 
            keeps user on the create listing page, but does not display 
            error message.

        NOTE: A warning flag is shown in this case, but it is not an 
              element on the website, so it's presence cannot be tested for. 
    
    
    T3: Utilises FUNCTIONALITY COVERAGE TESTING to test the system's actions
    
    Requirement partitions to be tested (based on A2):
      R1:
      - P1: Title is alphanumeric with no spaces as prefix or suffix
      - P2: Title is not alphanumeric
      - P3: Title has a space as a prefix
      - P4: Title has a space as a suffix

      R2:
      - P1: Title is shorter than 80 characters
      - P2: Title is longer than 80 characters

      R3:
      - P1: Description is less than 20 characters
      - P2: Description is between 20 and 2000 characters
      - P3: Description is more than 2000 characters

      R4:
      - P1: Description is longer than product's title
      - P2: Description is shorter than product's title

      R5: 
      - P1: Price is less than 10
      - P2: Price is between 10 and 10000
      - P3: Price is greater than 10000

      R6: Does not need frontend testing

      R7: Does not need frontend testing

      R8:
      - P1: User creates 2 listings with different names
      - P2: User creates 2 listings with the same name
    '''

    # Helper function to register a new user and log that user in.
    # This needs to be done before a listing can be created
    def create_user_and_login(self, name, email, password):
        ''' Register a user '''
        # Open registration page
        self.open(base_url + '/register')

        # valid email, name, and password
        self.type("#email", email)
        self.type("#name", name)
        self.type("#password", password)
        self.type("#password2", password)

        # submit registration form
        self.click('input[type="submit"]')

    # T1-P1, T1-P5, T1-P10, T2-P1, T3-R1-P1, T3-R2-P1, T3-R3-P2, 
    # T3-R4-P1, T3-R5-P2
    def test_title_correct(self, *_):
        self.create_user_and_login("Example0", "example0@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description, and price
        self.type("#title", "A Title")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Check that the user was redirected to the homepage 
        # and that there is a listing on the homepage
        self.assert_element("#welcome-header")
        self.assert_element("#listings")
        self.assert_text("A Title", "#title")

    # T1-P2, T2-P2, T3-R1-P2
    def test_not_alphanumeric(self, *_):
        self.create_user_and_login("Example1", "example1@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # invalid title, valid description and price
        self.type("#title", "A Title!")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Could not create listing.", "#message")

    # T1-P3, T2-P3
    def test_no_title(self, *_):
        self.create_user_and_login("Example2", "example2@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # no title, valid description and price
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")

    # T1-P4, T3-R2-P2
    def test_long_title(self, *_):
        self.create_user_and_login("Example3", "example3@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # long title, valid description and price
        title = "A long title" * 10
        self.type("#title", title)
        self.type("#description", "A description for the listing" * 10)
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Check that the title was cut to 80 characters
        self.assert_element("#welcome-header")
        self.assert_element("#listings")
        self.assert_text(title[:80], "#title")

    # T1-P6
    def test_no_description(self, *_):
        self.create_user_and_login("Example4", "example4@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # Valid title, no description, valid price
        self.type("#title", "A title")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")
    
    # T1-P7, T3-R3-P1
    def test_short_description(self, *_):
        self.create_user_and_login("Example5", "example5@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # Valid title, short description, valid price
        self.type("#title", "A title")
        self.type("#description", "Description")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")

    # T1-P8, T3-R3-P3
    def test_long_description(self, *_):
        self.create_user_and_login("Example6", "example6@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, long description, valid price
        description = "Description" * 200
        self.type("#title", "A title")
        self.type("#description", description)
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Check that the title was cut to 80 characters
        self.assert_element("#welcome-header")
        self.assert_element("#listings")
        self.assert_text(description[:2000], "#description")

    # T1-P9, T3-R4-P2
    def test_description_shorter_than_title(self, *_):
        self.create_user_and_login("Example7", "example7@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title. Description shorter than title. Valid price
        self.type("#title", "A Long Listing Title That is Longer Than the \
            Description")
        self.type("#description", "A description for this listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Could not create listing.", "#message")
    
    # T1-P11
    def test_no_price(self, *_):
        self.create_user_and_login("Example8", "example8@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description. No price
        self.type("#title", "A title")
        self.type("#description", "A description of the listing!")

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")

    # T1-P12, T3-R5-P1
    def test_low_price(self, *_):
        self.create_user_and_login("Example9", "example9@gmail.com", "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description. Low price
        self.type("#title", "A title")
        self.type("#description", "A description for the listing.")
        self.type("#price", 9)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")
    
    # T1-P13, T3-R5-P3
    def test_high_price(self, *_):
        self.create_user_and_login("Example10", "example10@gmail.com",
                                   "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description. High price
        self.type("#title", "A title")
        self.type("#description", "A description for the listing.")
        self.type("#price", 10001)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should still be on create_listing page with no message appearing
        self.assert_text("Create a New Listing!", "#header")
        self.assert_element_not_visible("#message")

    # T3-R1-P3   
    def test_prefix_space(self, *_):
        self.create_user_and_login("Example11", "example11@gmail.com",
                                   "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # invalid title, valid description and price
        self.type("#title", " A Title")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Could not create listing.", "#message")

    # T3-R1-P4   
    def test_suffix_space(self, *_):
        self.create_user_and_login("Example12", "example12@gmail.com",
                                   "Examp!3")

        # open create_listing page
        self.open(base_url + '/create_listing')

        # invalid title, valid description and price
        self.type("#title", "A Title ")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Could not create listing.", "#message")
    
    # T3-R8-P1
    def test_create_2_different_listings(self, *_):
        self.create_user_and_login("Example13", "example13@gmail.com",
                                   "Examp!3")

        # Create the first listing

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description, and price
        self.type("#title", "A Title 1")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Create the second listing

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description, and price
        self.type("#title", "A Title 2")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Check that the user was redirected to the homepage 
        # and that there are 2 listings on the homepage
        self.assert_element("#welcome-header")
        self.assert_element("#listings")
        self.assert_text("A Title 1")
        self.assert_text("A Title 2")        

    # T3-R8-P2
    def test_create_2_equal_listings(self, *_):
        self.create_user_and_login("Example14", "example14@gmail.com",
                                   "Examp!3")

        # Create the first listing

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid title, description, and price
        self.type("#title", "A Title 3")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Create the second listing

        # open create_listing page
        self.open(base_url + '/create_listing')

        # valid but duplicate title, description, and price
        self.type("#title", "A Title 3")
        self.type("#description", "A description for the listing")
        self.type("#price", 100)

        # submit create_listing form
        self.click('input[type="submit"]')

        # Should display an error
        self.assert_element("#message")
        self.assert_text("Could not create listing.", "#message")
        
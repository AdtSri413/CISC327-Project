All frontend unit tests are located in qbnb_tests/frontend. 

1. test_registration.py contains all the unit tests for the user registration page:
    - test_password_length_1: Password too short
    - test_password_length_2: Valid password (minimum valid length)
    - test_username_length_1: Username too short
    - test_username_length_2: Username too long
    - test_username_length_3: Valid username (minimum valid length)
    - test_username_length_4: Valid username (maximum valid length)
    
2. test_login.py contains all the unit tests for the login page.
    - test_login_1: All login parameters valid
    - test_login_2: Incorrect password
    
3. test_create_listing.py contains all the unit tests for the create_listing page.
    - test_title_correct:                   All parameters valid
    - test_not_alphanumeric:                Title of listing is not alphanumeric
    - test_no_title:                        Title box is left empty
    - test_long_title: Title                is too long
    - test_no_description:                  Description box is left empty
    - test_short_description:               Description is too short
    - test_long_description:                Description is too long
    - test_description_shorter_than_title:  Description is a valid length, but shorter than the title
    - test_no_price:                        Price box is left empty
    - test_low_price:                       Price is too low
    - test_high_price:                      Price is too high
    - test_prefix_space:                    Title begins with a space
    - test_suffix_space:                    Title ends with a space
    - test_create_2_different_listings:     Create 2 listings with different titles (Should pass)
    - test_create_2_equal_listings:         Create 2 listings with the same title (Should fail)
    
4. test_update_listing.py contains all the unit tests for the update_listing page.
    - test_edit_page_price_below: Price too low
    - test_edit_page_price_at:    Valid price
    - test_edit_page_price_above: Price too high
    - test_output_fail:           Invalid listing title
    - test_output_success:        All parameters valid
    - test_price_decrease:        Try reducing the listing price (should fail)
    - test_price_decrease:        Try increasing the listing price (should pass) (error in name was discovered after code was merged. Will create card for next sprint)
    - test_update_all_attributes: Change all attributes of a listing
    
5. test_update_user.py contains all the unit tests for the update_user page.
    - test_edit_page_nonalphanum_postal:  Invalid postal code (not alphanumeric)
    - test_edit_page_blank_postal:        Invalid postal code (try to replace postal code with a single space)
    - test_edit_page_valid_postal:        Valid postal code
    - test_output_fail:                   Invalid name
    - test_output_success:                Valid parameters
    - test_update_all_attributes:         Change all user attributes



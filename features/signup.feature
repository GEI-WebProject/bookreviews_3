Feature: Sign Up
    In order to be able to create reviews
    As a user
    I want to create an account


    Background: A user has not an account


    Scenario: A user creates an account
        Given I am on the main page
        And I click on "Sign up" link
        When I fill the account form with valid data
            | username | email         | password1 | password2 |
            | user     | hola@hola.com | pass12345 | pass12345 |
        And I click on the "Sign Up" button
        Then I am redirected to the main page
        And I am logged in as "user"

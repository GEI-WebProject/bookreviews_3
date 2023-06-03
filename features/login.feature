Feature: Log In
    In order to access my account
    As a user
    I want to log into my account

    Background: A user has an account
        Given Exists a user "user" with password "pass12345"

    Scenario: A user logs in
        Given I am on the main page
        When I click on "Log in" link
        Then I am in the login page
        And I login as user "user" with password "pass12345"
        And I am logged in as "user"





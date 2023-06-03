Feature: Update Review
    In order to update my opinion about a book
    As a user
    I want to update a review

  Background: There is one book, two users and one review
        Given Exists a book with title "Test Book" isbn "1111111111111" synopsis "This is a testing book!" genres "Fiction" language "English" cover "https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg" author "Test Author" publisher "Test Publisher"
        And Exists a user "user" with password "pass12345"
        And Exists a user "another_user" with password "pass12345"
        And Exists a review for the book "Test Book" posted by "user" with title "My first review!" body "Very good!" and rating "3"

    Scenario: A user who is not logged in can't update a review via 'Edit' button
        Given I am on the "Test Book" detail page
        Then I can't see the "Edit" button

    Scenario: A user who is not logged in can't update a review via url
        Given I access the url to edit a review of "Test Book"
        Then I am redirected to the login page

    Scenario: A logged in user updates a review
        Given I login as user "user" with password "pass12345"
        And I am on the "Test Book" detail page
        When I click on the "Edit" button
        And I fill in the review form with valid data
            | title                    | body             | rating |
            | My first edited review ! | Very good again! | 5      |
        And I submit the review form
        Then I'm viewing the reviews page for the book "Test Book"
        And My review is on top
            | title                    | body             | rating |
            | My first edited review ! | Very good again! | 5      |
        And There are "1" reviews
        And A "Review updated successfully!" message is shown


    Scenario: A logged in user can't update a review from another user
        Given I login as user "another_user" with password "pass12345"
        And I am on the "Test Book" detail page
        Then I can't see the "Edit" button
        And I can't update the review via url for the book "Test Book"
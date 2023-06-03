Feature: Delete Review
  In order to delete my opinion about a book
  As a user
  I want to delete my review


  Background: There is one book, two users and one review
    Given Exists a book with title "Test Book" isbn "1111111111111" synopsis "This is a testing book!" genres "Fiction" language "English" cover "https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg" author "Test Author" publisher "Test Publisher"
    And Exists a user "user" with password "pass12345"
    And Exists a user "another_user" with password "pass12345"
    And Exists a review for the book "Test Book" posted by "user" with title "My first review!" body "Very good!" and rating "3"

  Scenario: A user who is not logged in can't delete a review via 'Delete' button
    Given I am on the "Test Book" detail page
    Then I can't see the "Delete" button

  Scenario: A user who is not logged in can't delete a review via url
    Given I access the url to delete a review of "Test Book"
    Then I am redirected to the login page

  Scenario: A logged in user deletes a review
    Given I login as user "user" with password "pass12345"
    And I am on the "Test Book" detail page
    When I click on the "Delete" button
    And I confirm that I want to delete the review
    Then The review is not shown in the page
    And There are "0" reviews
    And A "Review deleted successfully!" message is shown

  Scenario: A logged in user can't delete a review from another user
    Given I login as user "another_user" with password "pass12345"
    And I am on the "Test Book" detail page
    Then I can't see the "Delete" button
    And I can't delete the review via url for the book "Test Book"


Feature: Search a book
    In order to get information about a book
    As a user
    I want to search a book

    Background: Exists one book
        Given Exists a book with title "Test Book" isbn "1111111111111" synopsis "This is a testing book!" genres "Fiction" language "English" cover "https://marketplace.canva.com/EAFMf17QgBs/1/0/1003w/canva-green-and-yellow-modern-book-cover-business-Ah-do4Y91lk.jpg" author "Test Author" publisher "Test Publisher"


    Scenario: A user searches a book
        Given I am on the main page
        When I write the title "Test Book" on the search bar
        Then I see the book "Test Book" in the results page

from django.test import TestCase
from django.contrib.auth.models import User
from bookapp.models import *
from reviews.models import *


class BookReviewTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")

        lang = Language.objects.create(name="English")
        auth = Author.objects.create(name="Test Author")
        publ = Publisher.objects.create(name="Test Publisher")
        genr = Genre.objects.create(name="Fiction")

        bookWithReviews = Book.objects.create(
            title="Book with reviews",
            ISBN="1" * 13,
            synopsis="Test Synopsis",
            language=lang,
            cover="",
            publisher=publ
        )
        bookWithReviews.authors.add(auth)
        bookWithReviews.genres.add(genr)

        bookWithoutReviews = Book.objects.create(
            title="Book without reviews",
            ISBN="2" * 13,
            synopsis="Test Synopsis",
            language=lang,
            cover="",
            publisher=publ
        )
        bookWithoutReviews.authors.add(auth)
        bookWithoutReviews.genres.add(genr)

        Review.objects.create(book=bookWithReviews, user=user1,
                              title="Title 1", body="Body 1", rating=2)
        Review.objects.create(book=bookWithReviews, user=user2,
                              title="Title 2", body="Body 2", rating=3)
        Review.objects.create(book=bookWithReviews, user=user3,
                              title="Title 3", body="Body 3", rating=5)

    def test_average_multiple_reviews(self):
        """The average rating for a Book with 3 reviews is properly computed"""
        book = Book.objects.get(title="Book with reviews")
        self.assertEqual(book.averageRating(), (2 + 3 + 5) / 3)

    def test_average_without_reviews(self):
        """The average rating for a Book without reviews is 0"""
        book = Book.objects.get(title="Book without reviews")
        self.assertEqual(book.averageRating(), 0)

from behave import *
from django.contrib.auth.models import User

from bookapp.models import *
from reviews.models import Review

use_step_matcher("parse")


@given('Exists a user "{username}" with password "{password}"')
def step_impl(context, username, password):
    User.objects.create_user(
        username=username, email='user@example.com', password=password)


@given(
    u'Exists a book with title "{title}" isbn "{isbn}" synopsis "{synopsis}" genres "{genre}" language "{language}" cover "{cover}" author "{author}" publisher "{publisher}"')
def step_impl(context, title, isbn, synopsis, genre, language, cover, author, publisher):
    lang = Language.objects.create(name=language)
    auth = Author.objects.create(name=author)
    publ = Publisher.objects.create(name=publisher)
    genr = Genre.objects.create(name=genre)

    book = Book.objects.create(
        title=title,
        ISBN=isbn,
        synopsis=synopsis,
        language=lang,
        cover=cover,
        publisher=publ
    )
    book.authors.add(auth)
    book.genres.add(genr)


@given(
    u'Exists a review for the book "{book_title}" posted by "{user}" with title "{title}" body "{body}" and rating "{rating}"')
def step_impl(context, book_title, user, title, body, rating):
    book = Book.objects.get(title=book_title)
    user = User.objects.get(username=user)
    Review.objects.create(book=book, user=user,
                          title=title, body=body, rating=rating)

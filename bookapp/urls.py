from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('books', BooksView.as_view(), name='books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('search/books', BookSearchView.as_view(), name='book_search'),
    path('authors', AuthorsView.as_view(), name='authors'),
    path('authors/<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('authors/<int:pk>/books', AuthorBooksView.as_view(), name='author_books'),
]

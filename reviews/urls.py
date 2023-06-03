from django.urls import path
from .views import *

urlpatterns = [
    path('reviews/', AllReviewsListView.as_view(), name="reviews"),
    path('reviews/<int:pk>', ReviewDetailView.as_view(), name="review_detail"),
    path('books/<int:book_id>/reviews', BookReviewsListView.as_view(), name="book_reviews"),
    path('books/<int:book_id>/reviews/new', CreateReviewView.as_view(), name="review_create"),
    path('books/<int:book_id>/reviews/<int:pk>/edit', UpdateReviewView.as_view(), name="review_update"),
    path('books/<int:book_id>/reviews/<int:pk>/delete', DeleteReviewView.as_view(), name="review_delete"),
]
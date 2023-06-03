from django.db import models
from django.contrib.auth.models import User
from bookapp.models import Book

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(max_length=50)
    body = models.TextField()
    rating = models.PositiveIntegerField(choices=(
        (1, 'Bad'),
        (2, 'Poor'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Excellent')
    ))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review: "{self.title}" by {self.user.username} on {self.book.title}'

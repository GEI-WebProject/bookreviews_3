from django.db import models
from django.db.models import Avg

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
         return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
         return self.name
    
    
class Author(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.URLField(max_length=200, null=True, default="https://openlibrary.org/images/icons/avatar_author-lg.png")

    def __str__(self):
         return self.name
     
    
class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
         return self.name
     
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    ISBN = models.CharField(max_length=13)
    synopsis = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    cover = models.URLField(max_length=200, null=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
         return self.title
     
    def averageRating(self):
        if not self.reviews.count():
            return 0
        else:
            return self.reviews.all().aggregate(Avg('rating'))['rating__avg']

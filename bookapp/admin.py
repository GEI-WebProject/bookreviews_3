from django.contrib import admin
from bookapp.models import *
# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
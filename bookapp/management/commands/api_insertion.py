from django.core.management.base import BaseCommand, CommandError
from bookapp.models import *
from bookapp.management.commands import _api_commands as api


class Command(BaseCommand):
    help = "Add books from API"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        self.stdout.write("Searching books...\n")
        books, authors = api.getBooksFromAPI()
        for a in authors:
            Author.objects.get_or_create(name=a.name, defaults={"birth_date": a.birth_date, "bio": a.bio, "picture": a.picture})
        for b in books:
            book, _ = Book.objects.get_or_create(title=b.title, 
                        ISBN=b.isbn, 
                        synopsis=b.synopsis,
                        language=Language.objects.get_or_create(name=b.language)[0],
                        cover=b.cover,
                        publisher=Publisher.objects.get_or_create(name=b.publisher)[0]
                        )
            book.genres.set([Genre.objects.get_or_create(name=genre)[0] for genre in b.genres])
            book.authors.set([Author.objects.get(name=author_name) for author_name in b.author])
        self.stdout.write("Finished!\n")
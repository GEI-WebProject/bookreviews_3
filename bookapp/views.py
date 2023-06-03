from django.views.generic import ListView, DetailView
from .models import Book, Author
from django.core.cache import cache
from django.utils import timezone
from random import sample


class HomeView(ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'

    def get_queryset(self):
        today = timezone.now().date()
        daily_books = cache.get(today)
        if not daily_books:
            SAMPLE = 5
            # If the cached random books for today don't exist, generate them and cache them for the day
            all_books = list(Book.objects.all())
            daily_books = sample(all_books, SAMPLE) if len(all_books) > SAMPLE else all_books
            cache.set(today, daily_books, 60 * 60 * 24)  # Cache for 24 hours
        return daily_books


class BooksView(ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('title')


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    REVIEWS_SHOWN = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_reviews'] = self.object.reviews.all().order_by('-updated_at')[:self.REVIEWS_SHOWN]
        context['num_reviews_shown'] = self.REVIEWS_SHOWN
        return context


class BookSearchView(ListView):
    model = Book
    template_name = 'books/book_search.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', None)
        if query:
            queryset = queryset.filter(
                title__icontains=query).order_by('title')
        else:
            queryset = Book.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class AuthorsView(ListView):
    model = Author
    template_name = 'authors/authors.html'
    context_object_name = 'authors'
    paginate_by = 3

    def get_queryset(self):
        return Author.objects.order_by('name')


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'
    context_object_name = 'author'


class AuthorBooksView(ListView):
    model = Book
    template_name = 'authors/author_books.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        return Book.objects.filter(authors=self.kwargs.get('pk'))

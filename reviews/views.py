from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ReviewForm
from bookapp.models import Book
from django.contrib import messages
from django.db.models import Case, When, Value, BooleanField


class AllReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "reviews/reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-updated_at')


class ReviewDetailView(DetailView):
    model = Review
    template_name = "reviews/review_detail.html"
    context_object_name = "review"


class BookReviewsListView(ListView):
    model = Review
    template_name = "reviews/book_reviews.html"
    context_object_name = "reviews"
    paginate_by = 2

    # Add get_queryset() method to filter reviews by book
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Review.objects.filter(book=self.kwargs['book_id']).order_by(
                Case(
                    When(user=self.request.user, then=Value(0)),
                    default=Value(1),
                    output_field=BooleanField(),
                ),
                '-updated_at'
            )
        else:
            return Review.objects.filter(book=self.kwargs['book_id']).order_by('-updated_at')

    # Add get_context_data() method to add book to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = "reviews/review_create.html"
    form_class = ReviewForm
    success_message = "Review created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['book_id']
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_reviews', kwargs={'book_id': self.kwargs['book_id']})


class UpdateReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    template_name = "reviews/review_update.html"
    form_class = ReviewForm
    success_message = "Review updated successfully!"

    def get_success_url(self):
        return reverse_lazy('book_reviews', kwargs={'book_id': self.kwargs['book_id']})

    def test_func(self):
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "reviews/review_delete.html"
    success_message = "Review deleted successfully!"

    def get_success_url(self):
        return reverse_lazy('book_reviews', kwargs={'book_id': self.kwargs['book_id']})

    def test_func(self):
        return self.request.user == self.get_object().user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

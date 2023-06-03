from behave import *


use_step_matcher("parse")


@then(u'I am redirected to the main page')
def step_impl(context):
    assert context.browser.url == context.get_url('home')


@given(u'I am on the main page')
def step_impl(context):
    context.browser.visit(context.get_url('home'))


@then(u'I am in the login page')
def step_impl(context):
    assert context.browser.url == context.get_url('login')


@given(u'I am on the "{book_title}" detail page')
def step_impl(context, book_title):
    from bookapp.models import Book
    book_id = Book.objects.get(title=book_title).id
    context.browser.visit(context.get_url('book_detail', pk=book_id))
from behave import *

use_step_matcher("parse")


@when(u'I click on "Create a new review" button')
def step_impl(context):
    context.browser.find_by_name('create_review_button').first.click()


@then(u'I am redirected to the login page')
def step_impl(context):
    browser_url = context.browser.url
    login_url = context.get_url('login')
    assert browser_url.startswith(login_url)


@then(u'I can\'t create the review via url for the book "{book_title}"')
def step_impl(context, book_title):
    from bookapp.models import Book
    book_id = Book.objects.get(title=book_title).id
    context.browser.visit(context.get_url('review_create', book_id=book_id))

    browser_url = context.browser.url
    login_url = context.get_url('login')
    assert browser_url.startswith(login_url)


@when(u'I fill in the review form with valid data')
def step_impl(context):
    for row in context.table:
        for heading in row.headings:
            if heading != "rating":
                context.browser.fill(heading, row[heading])
            else:
                script = f"""
                        var rateYoContainer = document.querySelector('.rateyo-interactive');
                        var hiddenInput = document.querySelector('#id_rating');
                        var event = new Event('rateyo.set', {{ bubbles: true }});

                        hiddenInput.value = '{row[heading]}';
                        rateYoContainer.dispatchEvent(event);
                        """
                context.browser.execute_script(script)


@when(u'I submit the review form')
def step_impl(context):
    context.browser.find_by_name("submit_button").first.click()


@then(u'I\'m viewing the reviews page for the book "{title}"')
def step_impl(context, title):
    from bookapp.models import Book
    book_id = Book.objects.get(title=title).id
    assert context.browser.url == context.get_url(
        "book_reviews", book_id=book_id)


@then(u'My review is on top')
def step_impl(context):
    title = context.table[0][0]
    body = context.table[0][1]
    assert title == context.browser.find_by_name("review_title").first.value
    assert body == context.browser.find_by_name("review_body").first.value


@then(u'There are "{reviews_count}" reviews')
def step_impl(context, reviews_count):
    from reviews.models import Review
    reviews = context.browser.find_by_name('review_card')
    assert len(reviews) == int(reviews_count)
    assert Review.objects.count() == int(reviews_count)
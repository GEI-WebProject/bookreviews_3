from behave import *


use_step_matcher("parse")


@when(u'I write the title "{title}" on the search bar')
def step_impl(context, title):
    form = context.browser.find_by_name('search_form').first
    context.browser.fill('q', title)
    form.find_by_tag('button').first.click()


@then(u'I see the book "{title}" in the results page')
def step_impl(context, title):
    assert context.browser.find_by_name('title').first.value == title

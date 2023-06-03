from behave import *


use_step_matcher("parse")


@given(u'I click on "Sign up" link')
def step_impl(context):
    context.browser.find_by_name('signup_link').first.click()


@when(u'I fill the account form with valid data')
def step_impl(context):
    form = context.browser.find_by_name('signup_form')
    for row in context.table:
        for heading in row.headings:
            context.browser.fill(heading, row[heading])


@when(u'I click on the "Sign up" button')
def step_impl(context):
    context.browser.find_by_name('signup_button').first.click()


@then(u'I am logged in as "{username}"')
def step_impl(context, username):
    user_section = context.browser.find_by_name('user_session').first.value
    assert user_section.find(username) != -1


@when(u'I click on "Log in" link')
def step_impl(context):
    context.browser.find_by_name("login_link").first.click()


@then('I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser.visit(context.get_url('login'))
    form = context.browser.find_by_name('login_form').first
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    form.find_by_name('login_button').first.click()


@given(u'I login as user "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser.visit(context.get_url('login'))
    form = context.browser.find_by_name('login_form').first
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    form.find_by_name('login_button').first.click()

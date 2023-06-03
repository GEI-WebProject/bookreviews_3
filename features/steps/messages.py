from behave import *

use_step_matcher("parse")


@then(u'A "{message}" message is shown')
def step_impl(context, message):
    assert not context.browser.find_by_value(message).is_empty()
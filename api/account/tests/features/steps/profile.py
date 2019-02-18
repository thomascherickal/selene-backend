from datetime import date
from http import HTTPStatus
import json

from behave import given, then, when
from hamcrest import assert_that, equal_to, has_item

from selene.api.testing import generate_auth_tokens
from selene.data.account import PRIVACY_POLICY


@given('an authenticated user')
def setup_authenticated_user(context):
    generate_auth_tokens(context)


@when('account endpoint is called to get user profile')
def call_account_endpoint(context):
    context.response = context.client.get('/api/account')


@then('user profile is returned')
def validate_response(context):
    assert_that(context.response.status_code, equal_to(HTTPStatus.OK))
    response_data = json.loads(context.response.data)
    assert_that(
        response_data['emailAddress'],
        equal_to(context.account.email_address)
    )
    assert_that(
        response_data['subscription']['type'],
        equal_to('Monthly Supporter')
    )
    assert_that(
        response_data['subscription']['startDate'],
        equal_to(str(date.today()))
    )
    assert_that(
        response_data['subscription'], has_item('id')
    )

    assert_that(len(response_data['agreements']), equal_to(1))
    agreement = response_data['agreements'][0]
    assert_that(agreement['type'], equal_to(PRIVACY_POLICY))
    assert_that(agreement['acceptDate'], equal_to(str(date.today())))
    assert_that(agreement, has_item('id'))

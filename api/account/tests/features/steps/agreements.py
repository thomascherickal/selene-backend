from dataclasses import asdict
from http import HTTPStatus
import json

from behave import then, when
from hamcrest import assert_that, equal_to


@when('API request for Privacy Policy is made')
def call_agreement_endpoint(context):
    context.response = context.client.get('/api/agreement/privacy-policy')


@then('version {version} of Privacy Policy is returned')
def validate_response(context, version):
    assert_that(context.response.status_code, equal_to(HTTPStatus.OK))
    response_data = json.loads(context.response.data)
    expected_response = asdict(context.privacy_policy)
    del(expected_response['effective_date'])
    assert_that(response_data, equal_to(expected_response))
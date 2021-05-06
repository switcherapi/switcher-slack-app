import os
import requests
import unittest
import json

from src.app import flask_app
from src.payloads.home import MODAL_REQUEST

from unittest.mock import patch
from nose.tools import assert_true

from slack_sdk.signature import SignatureVerifier

from tests.fixtures.installation import INSTALLATION_FIX1
from tests.fixtures.change_request import OPEN_CHANGE_REQUEST_MODAL_FIX1, get_slack_events_response
from tests.utils.mock_request import mock_requests_factory
from slack_sdk.web.base_client import BaseClient

def mock_get_installation(*args, **kwargs):
    return mock_requests_factory(json.dumps(INSTALLATION_FIX1), 200)

class SlackEventTest(unittest.TestCase):

    def setUp(self):
        self.flask_app = flask_app.test_client()
        self.callback_url = os.environ.get("SWITCHER_URL")

    def test_open_change_request_modal(self):
        with (
            # Bypass content verification
            patch.object(SignatureVerifier, "is_valid", return_value = True),

            # Mock installation
            patch.object(requests, "get", return_value = mock_get_installation),

            # Mock Slack API call
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            # When
            response = self.flask_app.post(f"/slack/events", json = OPEN_CHANGE_REQUEST_MODAL_FIX1)

            # Then
            self.assertEqual(200, response.status_code)

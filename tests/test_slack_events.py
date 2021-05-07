import os
import unittest

from src.app import flask_app
from src.payloads.home import MODAL_REQUEST

from unittest.mock import patch
from nose.tools import assert_true

from slack_sdk.web.base_client import BaseClient

from tests.utils.mock_request import mock_event_handler
from tests.fixtures.change_request import (
    OPEN_APP_HOME_FIX1, 
    OPEN_MODAL_CHANGE_REQUEST_FIX1,
    ENVIRONMENT_SELECTION_FIX1,
    get_slack_events_response
)

class SlackEventTest(unittest.TestCase):

    def setUp(self):
        self.flask_app = flask_app.test_client()
        self.callback_url = os.environ.get("SWITCHER_URL")

    @mock_event_handler
    def test_open_app_home(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(f"/slack/events", json = OPEN_APP_HOME_FIX1)
            self.assertEqual(200, response.status_code)


    @mock_event_handler
    def test_open_change_request_modal(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(f"/slack/events", json = OPEN_MODAL_CHANGE_REQUEST_FIX1)
            self.assertEqual(200, response.status_code)

    @mock_event_handler
    def test_open_change_request_modal(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(f"/slack/events", json = ENVIRONMENT_SELECTION_FIX1)
            self.assertEqual(200, response.status_code)
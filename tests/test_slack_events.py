import os
import unittest

from src.app import flask_app
from src.payloads.home import MODAL_REQUEST

from unittest.mock import patch
from nose.tools import assert_true

from tests.utils.mock_request import mock_event_handler, mock_base_client
from tests.fixtures.change_request import (
    OPEN_APP_HOME_FIX1,
    build_request_view,
    build_action_value,
    build_state_value
)

class SlackEventTest(unittest.TestCase):

    def setUp(self):
        self.flask_app = flask_app.test_client()
        self.callback_url = os.environ.get("SWITCHER_URL")

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_open_app_home(self):
        response = self.flask_app.post(f"/slack/events", json = OPEN_APP_HOME_FIX1)
        self.assertEqual(200, response.status_code)

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_open_change_request_modal(self):
        response = self.flask_app.post(
            f"/slack/events", json = build_request_view(
                actions_fixture = build_action_value(
                    action_id = "request_change",
                    text = "Request Change"
                )
            )
        )
        self.assertEqual(200, response.status_code)

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_select_evenvironment(self):
        response = self.flask_app.post(
            f"/slack/events", json = build_request_view(
                actions_fixture = build_action_value(
                    action_id = "selection_environment",
                    text = "Production",
                    value = "default"
                )
            )
        )
        self.assertEqual(200, response.status_code)

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_select_group(self):
        response = self.flask_app.post(
            f"/slack/events", json = build_request_view(
                actions_fixture = build_action_value(
                    action_id = "selection_group",
                    text = "Release 1",
                    value = "Release 1"
                )
            )
        )
        self.assertEqual(200, response.status_code)

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_select_switcher(self):
        response = self.flask_app.post(
            f"/slack/events", json = build_request_view(
                actions_fixture = build_action_value(
                    action_id = "selection_switcher",
                    text = "MY_FEATURE",
                    value = "MY_FEATURE"
                )
            )
        )
        self.assertEqual(200, response.status_code)

    @mock_event_handler
    @mock_base_client(MODAL_REQUEST)
    def test_select_status(self):
        response = self.flask_app.post(
            f"/slack/events", json = build_request_view(
                actions_fixture = build_action_value(
                    action_id = "selection_status",
                    text = "Activate",
                    value = "true"
                )
            )
        )
        self.assertEqual(200, response.status_code)
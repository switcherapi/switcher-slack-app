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
    build_request_view,
    build_action_value,
    build_state_value,
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
    def test_select_evenvironment(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(
                f"/slack/events", json = build_request_view(
                    actions_fixture = build_action_value(
                        action_id = "selection_environment",
                        text = "Production",
                        value = "default"
                    ),
                    state_fixture = build_state_value(
                        action_id = "selection_environment",
                        text = "Production",
                        value = "default"
                    )
                )
            )
            self.assertEqual(200, response.status_code)


    @mock_event_handler
    def test_select_group(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(
                f"/slack/events", json = build_request_view(
                    actions_fixture = build_action_value(
                        action_id = "selection_group",
                        text = "Release 1",
                        value = "Release 1"
                    ),
                    state_fixture = build_state_value(
                        action_id = "selection_group",
                        text = "Release 1",
                        value = "Release 1"
                    )
                )
            )
            self.assertEqual(200, response.status_code)

    @mock_event_handler
    def test_select_switcher(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(
                f"/slack/events", json = build_request_view(
                    actions_fixture = build_action_value(
                        action_id = "selection_switcher",
                        text = "MY_FEATURE",
                        value = "MY_FEATURE"
                    ),
                    state_fixture = build_state_value(
                        action_id = "selection_switcher",
                        text = "MY_FEATURE",
                        value = "MY_FEATURE"
                    )
                )
            )
            self.assertEqual(200, response.status_code)

    @mock_event_handler
    def test_select_status(self):
        with (
            patch.object(BaseClient, '_urllib_api_call', return_value = get_slack_events_response(
                req_args = MODAL_REQUEST,
                data = MODAL_REQUEST
            ))
        ):
            response = self.flask_app.post(
                f"/slack/events", json = build_request_view(
                    actions_fixture = build_action_value(
                        action_id = "selection_status",
                        text = "Activate",
                        value = "true"
                    ),
                    state_fixture = build_state_value(
                        action_id = "selection_status",
                        text = "Activate",
                        value = "true"
                    )
                )
            )
            self.assertEqual(200, response.status_code)
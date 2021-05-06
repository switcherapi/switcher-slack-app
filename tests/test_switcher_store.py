import os
import requests
import unittest

from src.app import flask_app

from unittest.mock import patch
from nose.tools import assert_true

from slack_bolt.oauth import OAuthFlow
from slack_sdk.oauth.installation_store.models.installation import Installation
from slack_sdk.oauth.state_utils import OAuthStateUtils
from slack_sdk.oauth.state_store import FileOAuthStateStore

from tests.fixtures.installation import INSTALLATION_FIX1
from tests.utils.mock_request import mock_requests_factory

def mock_created(*args, **kwargs):
    return mock_requests_factory("{}", 201)

class SwitcherStoreTest(unittest.TestCase):

    def setUp(self):
        self.flask_app = flask_app.test_client()
        self.callback_url = os.environ.get("SWITCHER_URL")

    def test_save_installation_success(self):
        with (
            # Bypass browser and state validations
            patch.object(OAuthStateUtils, 'is_valid_browser', return_value = True), 
            patch.object(FileOAuthStateStore, 'consume', return_value = True),

            # Inject Installation result
            patch.object(OAuthFlow, 'run_installation', return_value = Installation(**INSTALLATION_FIX1)),

            # Inject Store API mocked response
            patch.object(requests, 'post', return_value = mock_created)
        ):
            path = "/slack/oauth_redirect"

            # When
            response = self.flask_app.get(f"{path}?code=123")

            # Then
            e_id = INSTALLATION_FIX1["enterprise_id"]
            t_id = INSTALLATION_FIX1["team_id"]
            ch = INSTALLATION_FIX1["incoming_webhook_channel"]
            ch_id = INSTALLATION_FIX1["incoming_webhook_channel_id"]

            self.assertEqual(308, response.status_code)
            self.assertEqual(
                f"{self.callback_url}{path}?e_id={e_id}&t_id={t_id}&ch={ch}&chid={ch_id}",
                response.headers["Location"]
            )

    def test_save_installation_invalid_store(self):
        with (
            # Bypass browser validation
            patch.object(OAuthStateUtils, 'is_valid_browser', return_value = True), 

            # Force invalid state
            patch.object(FileOAuthStateStore, 'consume', return_value = False),
        ):
            # Test
            response = self.flask_app.get("/slack/oauth_redirect?code=123")

            # Then
            self.assertEqual(308, response.status_code)
            self.assertEqual(f"{self.callback_url}/slack/error", response.headers["Location"])

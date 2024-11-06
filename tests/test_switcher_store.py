import os
import pytest

from src.app import slack_app

from unittest.mock import patch

from slack_bolt.oauth import OAuthFlow
from slack_sdk.oauth.installation_store.models.installation import Installation
from slack_sdk.oauth.state_utils import OAuthStateUtils
from slack_sdk.oauth.state_store import FileOAuthStateStore

from tests.fixtures.installation import INSTALLATION_FIX1
from tests.utils.mock_request import (
    mock_event_handler, 
    mock_switcher_client
)

callback_url = os.environ.get("SWITCHER_URL")

@pytest.fixture
def client():
    slack_app.config['TESTING'] = True
    with slack_app.test_client() as client:
        yield client

@mock_event_handler
def test_health(client):
    response = client.get("/check")
    assert response.status_code == 200
    assert response.get_json()['status'] == 'UP'

@mock_event_handler
def test_save_installation_success(client):
    with (
        # Bypass browser and state validations
        patch.object(OAuthStateUtils, 'is_valid_browser', return_value = True), 
        patch.object(FileOAuthStateStore, 'consume', return_value = True),

        # Inject Installation result
        patch.object(OAuthFlow, 'run_installation', return_value = Installation(**INSTALLATION_FIX1)),
    ):
        path = "/slack/oauth_redirect"

        # When
        response = client.get(f"{path}?code=123")

        # Then
        e_id = INSTALLATION_FIX1["enterprise_id"]
        t_id = INSTALLATION_FIX1["team_id"]

        assert response.status_code == 308
        assert f"{callback_url}/slack/authorization?e_id={e_id}&t_id={t_id}" == response.headers["Location"]

@mock_switcher_client("post", {}, 400)
def test_save_installation_fail(client):
    with (
        # Bypass browser and state validations
        patch.object(OAuthStateUtils, 'is_valid_browser', return_value = True), 
        patch.object(FileOAuthStateStore, 'consume', return_value = True),

        # Inject Installation result
        patch.object(OAuthFlow, 'run_installation', return_value = Installation(**INSTALLATION_FIX1)),
    ):
        path = "/slack/oauth_redirect"
        response = client.get(f"{path}?code=123")
        assert response.status_code == 308

def test_save_installation_invalid_store(client):
    with (
        # Bypass browser validation
        patch.object(OAuthStateUtils, 'is_valid_browser', return_value = True), 

        # Force invalid state
        patch.object(FileOAuthStateStore, 'consume', return_value = False),
    ):
        # Test
        response = client.get("/slack/oauth_redirect?code=123")

        # Then
        assert response.status_code == 308
        assert f"{callback_url}/slack/authorization?error=1&reason=invalid_state" == response.headers["Location"]

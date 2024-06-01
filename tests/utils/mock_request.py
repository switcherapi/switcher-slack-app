import json
import requests

from functools import wraps

from gql import Client

from unittest.mock import Mock
from unittest import mock
from unittest.mock import patch

from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.base_client import BaseClient
from slack_sdk.web.client import WebClient

from tests.fixtures.installation import INSTALLATION_FIX1
from tests.fixtures.change_request import get_slack_events_response

mock_response = mock.Mock(**{})
mock_response_path = ""

def set_mock_response(path: str, fixture: dict, status_code: int = 200):
    global mock_response
    global mock_response_path

    mock_response_path = path
    mock_response = mock_requests_factory(json.dumps(fixture), status_code)

def mock_requests_factory(response_stub: str, status_code: int = 200):
    return mock.Mock(**{
        "json.return_value": json.loads(response_stub),
        "text.return_value": response_stub,
        "content": response_stub,
        "status_code": status_code,
        "ok": status_code == 200
    })

def mock_source_api(*args, **kwargs):
    if kwargs["url"].endswith("slack/v1/installation"):
        return mock_requests_factory("", 201)

    if kwargs["url"].endswith("slack/v1/findinstallation"):
        return mock_requests_factory(json.dumps(INSTALLATION_FIX1), 200)

    if kwargs["url"].endswith(mock_response_path):
        return mock_response

def mock_event_handler(fn):
    """Bypass content verification and find installation"""
    @wraps(fn)
    def wrapper(client, *args, **kwargs):
        WebClient.views_publish = Mock()
        WebClient.chat_postMessage = Mock()
        WebClient.chat_update = Mock()
        WebClient.views_open = Mock()
        
        with (
            patch.object(SignatureVerifier, "is_valid", return_value = True),
            patch.object(requests, "get", side_effect = mock_source_api),
            patch.object(requests, 'post', side_effect = mock_source_api),
        ):
            return fn(client)
    return wrapper

def mock_base_client(data: dict):
    def mock_decorator(fn):
        @wraps(fn)
        def wrapper(client, *args, **kwargs):
            with (
                patch.object(BaseClient, 'api_call', 
                    return_value = get_slack_events_response(data)
                )
            ):
                fn(client, *args, **kwargs)
        return wrapper
    return mock_decorator

def mock_gql_client(fixture: dict):
    def mock_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with (
                patch.object(Client, '__init__', return_value = None),
                patch.object(Client, 'execute', return_value = fixture)
            ):
                fn(*args, **kwargs)
        return wrapper
    return mock_decorator

def mock_switcher_client(method: str, fixture: dict, status: int = 200):
    def mock_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with (
                patch.object(requests, method, return_value = mock_requests_factory(json.dumps(fixture), status))
            ):
                fn(*args, **kwargs)
        return wrapper
    return mock_decorator
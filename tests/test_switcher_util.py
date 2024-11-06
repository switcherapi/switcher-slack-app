import os
import pytest

from src.utils.switcher_util import (
    get_environment_keyval,
    get_keyval,
    validate_context_request
)

def test_get_environment_keyval():
    expected = [
        { "name": "Production", "value": "default" },
        { "name": "QA", "value": "QA" }
    ]
    assert expected == get_environment_keyval(["default", "QA"])

def test_get_keyval():
    RELEASE1 = "Release 1"
    
    expected = [
        { "name": f"[on] {RELEASE1}", "value": RELEASE1 }
    ]
    assert expected == get_keyval("name", [{"name": RELEASE1, "activated": True}])

def test_validate_context_request():
    with pytest.raises(Exception) as e_info:
        validate_context_request({})

    assert e_info.value.args[0] == "Missing [Domain - Domain ID - Environment - Group - Status]"

def test_env_loading():
    assert os.environ.get("SLACK_SIGNING_SECRET") == "[SLACK_SIGNING_SECRET]"
    assert os.environ.get("SLACK_CLIENT_ID") == "[SLACK_CLIENT_ID]"
    assert os.environ.get("SLACK_CLIENT_SECRET") == "[SLACK_CLIENT_SECRET]"
    assert os.environ.get("SWITCHER_URL") == "https://cloud.swiktcherapi.com"
    assert os.environ.get("SWITCHER_API_URL") == "https://switcherapi.com/api"
    assert os.environ.get("SWITCHER_JWT_SECRET") == "[SWITCHER_JWT_SECRET]"
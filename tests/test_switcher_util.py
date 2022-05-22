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
    { "name": RELEASE1, "value": RELEASE1 }
  ]
  assert expected == get_keyval("name", [{"name": RELEASE1, "activated": True}])

def test_validate_context_request():
  with pytest.raises(Exception) as e_info:
    validate_context_request({})

  assert e_info.value.args[0] == "Missing [Environment - Group - Status]"
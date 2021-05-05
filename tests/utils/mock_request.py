import json

from unittest.mock import Mock
from unittest import mock

def mock_requests_factory(response_stub: str, status_code: int = 200):
    return mock.Mock(**{
        'json.return_value': json.loads(response_stub),
        'text.return_value': response_stub,
        'status_code': status_code,
        'ok': status_code == 200
    })
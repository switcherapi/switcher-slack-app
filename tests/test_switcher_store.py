import requests

from dotenv import load_dotenv
from unittest import mock
from nose.tools import assert_true, raises

from slack_sdk.oauth.installation_store.models.installation import Installation
from src.store.switcher_store import SwitcherAppInstallationStore
from src.services.switcher_service import SwitcherService

from tests.fixtures import INSTALLATION_FIX1
from tests.utils.mock_request import mock_requests_factory

load_dotenv()

def mock_created(*args, **kwargs):
    return mock_requests_factory("{}", 201)

def test_install():
    with mock.patch.object(requests, 'post') as requests_post_mock:
        requests_post_mock.side_effect = mock_created

        store = SwitcherAppInstallationStore()
        installation = Installation(**INSTALLATION_FIX1)
        store.save(installation)

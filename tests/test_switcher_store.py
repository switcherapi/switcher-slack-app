import pytest

from pytest_mock import mocker
from mock import Mock, patch

from slack_sdk.oauth.installation_store.models.installation import Installation
from src.store.switcher_store import SwitcherAppInstallationStore

from .fixtures import INSTALLATION_FIX1

class TestClass():
    store = SwitcherAppInstallationStore()
    
    def test_save_installation(self, mocker):
        installation = Installation(**INSTALLATION_FIX1)
        self.store.save(installation)
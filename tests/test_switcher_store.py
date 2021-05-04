import sys
sys.path.insert(0, '../src')

import pytest
from src.store.switcher_store import SwitcherAppInstallationStore

class TestClass():
    store = SwitcherAppInstallationStore()

    def test(self):
        assert True
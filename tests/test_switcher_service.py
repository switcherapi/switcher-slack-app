import pytest

from src.services.switcher_service import SwitcherService

from tests.utils.mock_request import mock_gql_client

@pytest.fixture
def switcher_service():
    return SwitcherService()

@mock_gql_client({
    'configuration': {
        'environments': ['default', 'development', 'staging']
    }
})
def test_get_environments(switcher_service):
    expected = ['default', 'development', 'staging']
    assert expected == switcher_service.get_environments(
        team_id = "TEAM_ID"
    )

@mock_gql_client({
    'configuration': {
        'group': [
            {'name': 'Release 1', 'activated': True}
        ]
    }
})
def test_get_groups(switcher_service):
    expected = [{'name': 'Release 1', 'activated': True}]
    assert expected == switcher_service.get_groups(
        team_id = "TEAM_ID",
        environment = "default"
    )

@mock_gql_client({
    'configuration': {
        'config': [
            {'key': 'FEATURE01', 'activated': False}
        ]
    }
})
def test_get_switchers(switcher_service):
    switchers = switcher_service.get_switchers(
        team_id = "TEAM_ID",
        environment = "default",
        group = "Release 1"
    )
    assert 'FEATURE01' == switchers[0]['key']
    assert False == switchers[0]['activated']
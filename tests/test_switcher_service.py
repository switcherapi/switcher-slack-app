import pytest

from src.services.switcher_service import SwitcherService

from tests.utils.mock_request import mock_gql_client, mock_switcher_client_post

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

@mock_switcher_client_post('post', { 'message': 'Ticket verified' })
def test_validate_ticket(switcher_service):
    switcher_service.validate_ticket(
        team_id = "TEAM_ID", 
        context = {
            "environment": "default",
            "group": "Group",
            "switcher": "FEATURE",
            "status": "False",
        })

@mock_switcher_client_post('post', {'error': 'Switcher not found'}, 404)
def test_validate_ticket_invalid(switcher_service):
    with pytest.raises(Exception) as e_info:
        switcher_service.validate_ticket(
            team_id = "TEAM_ID", 
            context = {
                "environment": "default",
                "group": "Group",
                "switcher": "FEATURE",
                "status": "False",
            })

    assert e_info.value.args[0] == "Switcher not found"
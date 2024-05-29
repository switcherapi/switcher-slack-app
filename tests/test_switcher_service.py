import pytest

from src.services.switcher_service import SwitcherService
from src.errors import SwitcherValidationError

from tests.utils.mock_request import mock_gql_client, mock_switcher_client

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
        team_id = "TEAM_ID",
        domain_id = "DOMAIN_ID"
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
        domain_id = "DOMAIN_ID",
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
        domain_id = "DOMAIN_ID",
        environment = "default",
        group = "Release 1"
    )
    assert 'FEATURE01' == switchers[0]['key']
    assert False == switchers[0]['activated']

@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'VALIDATED' })
def test_validate_ticket(switcher_service):
    response = switcher_service.validate_ticket(
        team_id = "TEAM_ID", 
        context = {
            "domain_id": "1",
            "environment": "default",
            "group": "Group",
            "switcher": "FEATURE",
            "status": "False",
        })

    assert response == 'VALIDATED'

@mock_switcher_client('post', {'error': 'Switcher not found'}, 404)
def test_validate_ticket_invalid(switcher_service):
    with pytest.raises(Exception) as e_info:
        switcher_service.validate_ticket(
            team_id = "TEAM_ID", 
            context = {
                "domain_id": "1",
                "environment": "default",
                "group": "Group",
                "switcher": "FEATURE",
                "status": "False",
            })

    assert e_info.value.args[0] == "Switcher not found"

@mock_switcher_client('post', {
        'channel_id': 'CHANNEL_ID',
        'channel': 'APPROVAL',
        'ticket': { '_id': 'ticket_123' }
    }, status = 201
)
def test_create_ticket(switcher_service):
    switcher_service.create_ticket(
        team_id = "TEAM_ID", 
        context = {
            "domain_id": "1",
            "environment": "default",
            "group": "Group",
            "switcher": "FEATURE",
            "status": "False",
            "observations": "Deactivate FEATURE"
        }
    )

@mock_switcher_client('post', {'error': 'Some error message'}, 400)
def test_create_ticket_fail(switcher_service):
    with pytest.raises(Exception) as e_info:
        switcher_service.create_ticket(
            team_id = "TEAM_ID", 
            context = {
                "domain_id": "1",
                "environment": "default",
                "group": "Group",
                "switcher": "FEATURE",
                "status": "False",
                "observations": "Deactivate FEATURE"
            }
        )

    assert e_info.value.args[0] == "Some error message"

@mock_switcher_client('post', {'message': 'Ticker ticket123 processed'})
def test_approve_request(switcher_service):
    switcher_service.approve_request(
        team_id = "TEAM_ID", 
        domain_id = "DOMAIN_ID",
        ticket_id = "ticket123"
    )

@mock_switcher_client('post', {'message': 'Ticker ticket123 processed'})
def test_deny_request(switcher_service):
    switcher_service.deny_request(
        team_id = "TEAM_ID", 
        domain_id = "DOMAIN_ID",
        ticket_id = "ticket123"
    )

@mock_switcher_client('post', {}, 400)
def test_process_ticket_invalid(switcher_service):
    with pytest.raises(Exception) as e_info:
        switcher_service.deny_request(
            team_id = "TEAM_ID", 
            domain_id = "DOMAIN_ID",
            ticket_id = "ticket123"
        )

    assert e_info.value.args[0] == "Try it again later"
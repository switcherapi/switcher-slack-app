import json
import pytest
import logging
from unittest.mock import Mock

from src.controller.home import on_home_opened, on_change_request_opened
from src.controller.change_request import (
    on_domain_selected,
    on_environment_selected,
    on_group_selected,
    on_switcher_selected,
    on_change_request_review,
    on_submit,
    on_request_approved,
    on_request_denied
)
from src.payloads.home import APP_HOME
from tests.utils.mock_request import (
    mock_gql_client,
    mock_switcher_client
)
from tests.fixtures.change_request import (
    SWITCHER_STATE_SELECTION,
    build_request_view,
    build_request_message_view,
    build_static_select_action_value,
    build_buttom_action_value,

    # Constants 
    RELEASE_1,
    PRODUCTION,
    DEFAULT_ENV,
    MY_FEATURE,

    ON_CHANGE_REQUEST_OPENED,
    ON_DOMAIN_SELECTED,
    ON_ENVIRONMENT_SELECTED,
    ON_GROUP_SELECTED,
    ON_SWITCHER_SELECTED,
    ON_CHANGE_REQUEST_REVIEW,
    ON_SUBMIT,
    ON_REQUEST_APPROVED,
    ON_REQUEST_DENIED
)

@pytest.fixture
def client():
    client = Mock()
    client.views_publish = Mock()
    client.views_open = Mock()
    return client

def test_open_app_home(client):
    result = on_home_opened(client, event = build_request_view(
        actions_fixture = build_buttom_action_value(
            action_id = "open_change_request",
            text = "Request Change"
        )
    ), logger = logging.getLogger())

    assert result == APP_HOME

@mock_switcher_client('get', [{ 'name': 'Domain Name', 'id': '1' }])
def test_open_change_request_modal(client):
    result = on_change_request_opened(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_buttom_action_value(
                action_id = "change_request",
                text = "Request Change"
            )
        ),
        client = client,
        logger = logging.getLogger()
    )
    
    with open(ON_CHANGE_REQUEST_OPENED) as f:
        expected_result = json.load(f)

    assert result == expected_result

@mock_switcher_client('get', { 'error': 'Server unavailable' }, 500)
def test_open_change_request_modal_with_error(client):
    result = on_change_request_opened(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_buttom_action_value(
                action_id = "change_request",
                text = "Request Change"
            )
        ),
        client = client,
        logger = logging.getLogger()
    )
    
    assert result == None
    
@mock_gql_client({ 
    'configuration': { 
        'environments': ['default'] 
    }
})
def test_select_domain(client):
    with open(ON_CHANGE_REQUEST_OPENED) as f:
        modal = json.load(f)

    result = on_domain_selected(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_domain",
                text = "Domain",
                value = "1"
            ),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        logger = logging.getLogger()
    )

    with open(ON_DOMAIN_SELECTED) as f:
        expected_result = json.load(f)

    assert result == expected_result

@mock_gql_client({
    'configuration': {
        'group': [{'name': 'Release 1', 'activated': True}]
    }
})
def test_select_evironment(client):
    with open(ON_DOMAIN_SELECTED) as f:
        modal = json.load(f)

    result = on_environment_selected(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_environment",
                text = PRODUCTION,
                value = DEFAULT_ENV
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        logger = logging.getLogger()
    )

    with open(ON_ENVIRONMENT_SELECTED) as f:
        expected_result = json.load(f)

    assert result == expected_result

@mock_gql_client({
    'configuration': {
        'config': [{'key': 'FEATURE01', 'activated': False}]
    }
})
def test_select_group(client):
    with open(ON_ENVIRONMENT_SELECTED) as f:
        modal = json.load(f)

    result = on_group_selected(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_group",
                text = RELEASE_1,
                value = RELEASE_1
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        logger = logging.getLogger()
    )
    
    with open(ON_GROUP_SELECTED) as f:
        expected_result = json.load(f)

    assert result == expected_result

def test_select_switcher(client):
    with open(ON_GROUP_SELECTED) as f:
        modal = json.load(f)

    result = on_switcher_selected(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_switcher",
                text = MY_FEATURE,
                value = MY_FEATURE
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client
    )

    with open(ON_SWITCHER_SELECTED) as f:
        expected_result = json.load(f)

    assert result == expected_result

@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'VALIDATED' })
def test_submit_for_review(client):
    with open(ON_SWITCHER_SELECTED) as f:
        modal = json.load(f)

    result, user_message = on_change_request_review(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        view = build_request_message_view(
            state_fixture = SWITCHER_STATE_SELECTION
        ),
        logger = logging.getLogger()
    )

    with open(ON_CHANGE_REQUEST_REVIEW) as f:
        expected_result = json.load(f)

    assert result == expected_result
    assert user_message == None

@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'IGNORED_ENVIRONMENT' })
def test_submit_without_approval_ignored(client):
    with open(ON_SWITCHER_SELECTED) as f:
        modal = json.load(f)

    result, user_message = on_change_request_review(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        view = build_request_message_view(
            state_fixture = SWITCHER_STATE_SELECTION
        ),
        logger = logging.getLogger()
    )

    with open(ON_CHANGE_REQUEST_REVIEW) as f:
        expected_result = json.load(f)

    assert result == expected_result
    assert user_message == ":large_green_square: *Request does not require approval*: Updated with success!"

@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'FROZEN_ENVIRONMENT' })
def test_submit_without_approval_frozen(client):
    with open(ON_SWITCHER_SELECTED) as f:
        modal = json.load(f)

    result, user_message = on_change_request_review(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client,
        view = build_request_message_view(
            state_fixture = SWITCHER_STATE_SELECTION
        ),
        logger = logging.getLogger()
    )

    with open(ON_CHANGE_REQUEST_REVIEW) as f:
        expected_result = json.load(f)

    assert result == expected_result
    assert user_message == ":large_red_square: *Request cannot be made*: Environment is frozen."

@mock_switcher_client('post', {
        'channel_id': 'CHANNEL_ID',
        'channel': 'APPROVAL',
        'ticket': { '_id': 'ticket_123' }
    }, status = 201
)
def test_submit_request(client):
    with open(ON_CHANGE_REQUEST_REVIEW) as f:
        modal = json.load(f)

    result, ticket = on_submit(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            ),
            blocks_fixture = modal['blocks'],
            private_metadata = modal['private_metadata']
        ),
        client = client,
        logger = logging.getLogger()
    )

    with open(ON_SUBMIT) as f:
        expected_result = json.load(f)

    assert result == expected_result
    assert ticket == { 'ticket_id': 'ticket_123', 'channel_id': 'CHANNEL_ID' }

@mock_switcher_client('post', {'message': 'Ticker ticket123 processed'})
def test_approve_request(client):
    result = on_request_approved(
        ack = Mock(),
        body = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_approved",
                text = "Approve",
                value = json.dumps({ 'id': 'ticket_123', 'domain_id': '1' })
            )
        ),
        client = client,
        logger = logging.getLogger()
    )

    with open(ON_REQUEST_APPROVED) as f:
        expected_result = json.load(f)

    assert result == expected_result

@mock_switcher_client('post', {'message': 'Ticker ticket123 processed'})
def test_deny_request(client):
    result = on_request_denied(
        ack = Mock(),
        body = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_denied",
                text = "Deny",
                value = json.dumps({ 'id': 'ticket_123', 'domain_id': '1' })
            )
        ),
        client = client,
        logger = logging.getLogger()
    )

    with open(ON_REQUEST_DENIED) as f:
        expected_result = json.load(f)

    assert result == expected_result
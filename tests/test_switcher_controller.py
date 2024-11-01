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
    mock_gql_client_error,
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
    ON_SWITCHER_SELECTED_NONE,
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
    """ Should open the app home view """

    result = on_home_opened(client, event = build_request_view(
        actions_fixture = build_buttom_action_value(
            action_id = "open_change_request",
            text = "Request Change"
        )
    ), logger = logging.getLogger())

    assert result == APP_HOME

@mock_switcher_client('get', [{ 'name': 'Domain Name', 'id': '1' }])
def test_open_change_request_modal(client):
    """ Should open the change request modal """

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

    result = __remove_block_id(result)
    assert result == expected_result

@mock_switcher_client('get', { 'error': 'Server unavailable' }, 500)
def test_open_change_request_modal_with_error(client):
    """ Should return None when server is unavailable """

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
    """ Should load environments when domain is selected """

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
    
    result = __remove_block_id(result)
    assert result == expected_result

@mock_gql_client_error()
def test_select_domain_error(client):
    """ Should not load environments when API returns an error """

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
    
    assert "Error opening change request form" in result

@mock_gql_client({
    'configuration': {
        'group': [{'name': 'Release 1', 'activated': True}]
    }
})
def test_select_evironment(client):
    """ Should load groups when environment is selected """

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

    result = __remove_block_id(result)
    assert result == expected_result

@mock_gql_client_error()
def test_select_evironment_error(client):
    """ Should not load groups when API returns an error """

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

    assert "Error selecting environment" in result

@mock_gql_client({
    'configuration': {
        'config': [{'key': 'FEATURE01', 'activated': False}]
    }
})
def test_select_group(client):
    """ Should load switchers and status when group is selected """

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

    result = __remove_block_id(result)
    assert result == expected_result

@mock_gql_client_error()
def test_select_group_error(client):
    """ Should not load switchers and status when API returns an error """

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
    
    assert "Error selecting group" in result

def test_select_switcher(client):
    """ Should load status when switcher is selected """

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

    result = __remove_block_id(result)
    assert result == expected_result

def test_select_switcher_none(client):
    """ Should load status based on Group selection when selected switcher is '-' """

    with open(ON_GROUP_SELECTED) as f:
        modal = json.load(f)

    result = on_switcher_selected(
        ack = Mock(),
        body = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_switcher",
                text = "-",
                value = "-"
            ),
            state_fixture = SWITCHER_STATE_SELECTION,
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            }),
            blocks_fixture = modal['blocks']
        ),
        client = client
    )

    with open(ON_SWITCHER_SELECTED_NONE) as f:
        expected_result = json.load(f)

    result = __remove_block_id(result)
    assert result == expected_result

@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'VALIDATED' })
def test_submit_for_review(client):
    """ Should open the request review """

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
    """ Should return a message when request does not require approval """

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
    """ Should return a message when environment is frozen """

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

@mock_switcher_client('post', { 'error': 'Server unavailable' }, 500)
def test_submit_for_review_error(client):
    """ Should return an error message when server is unavailable """

    with open(ON_SWITCHER_SELECTED) as f:
        modal = json.load(f)

    result = on_change_request_review(
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

    assert "Error on change request review" in result

@mock_switcher_client('post', {
        'channel_id': 'CHANNEL_ID',
        'channel': 'APPROVAL',
        'ticket': { '_id': 'ticket_123' }
    }, status = 201
)
def test_submit_request(client):
    """ Should submit the request for approval """

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
    """ Should approve the request """

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
    """ Should deny the request """

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

# Helper functions

def __remove_block_id(result):
    for block in result["blocks"]:
        if block.get("block_id"):
            del block["block_id"]
    return result
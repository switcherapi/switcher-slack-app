import os
import json
import pytest

from src.app import flask_app
from src.services.switcher_service import SwitcherService
from src.payloads.home import MODAL_REQUEST

from tests.utils.mock_request import (
    mock_event_handler,
    mock_base_client, 
    mock_gql_client,
    mock_switcher_client
)
from tests.fixtures.change_request import (
    SLACK_EVENT,
    OPEN_APP_HOME_FIX1,
    GROUP_STATE_SELECTION,
    SWITCHER_STATE_SELECTION,
    build_request_view,
    build_request_message_view,
    build_static_select_action_value,
    build_buttom_action_value,
    build_text_state_value,
    build_static_select_state_value,

    # Constants 
    RELEASE_1,
    PRODUCTION,
    DEFAULT_ENV,
    MY_FEATURE,
    MY_FEATURE1,
    OBSERVATION
)

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_open_app_home(client):
    response = client.post(SLACK_EVENT, json = OPEN_APP_HOME_FIX1)
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_open_change_request_modal(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "change_request",
                text = "Request Change"
            )
        )
    )
    assert response.status_code == 200

@mock_gql_client({ 
    'configuration': { 
        'environments': ['default'] 
    }
})
@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_domain(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_domain",
                text = "Test",
                value = "1"
            )
        )
    )
    assert response.status_code == 200


@mock_gql_client({
    'configuration': {
        'group': [{'name': 'Release 1', 'activated': True}]
    }
})
@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_evironment(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_environment",
                text = PRODUCTION,
                value = DEFAULT_ENV
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_gql_client({
    'configuration': {
        'config': [{'key': 'FEATURE01', 'activated': False}]
    }
})
@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_group(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_group",
                text = RELEASE_1,
                value = RELEASE_1
            ),
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_switcher(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_switcher",
                text = MY_FEATURE,
                value = MY_FEATURE
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_select_status(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "selection_status",
                text = "Activate",
                value = "true"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'VALIDATED' })
def test_submit_for_review(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            req_type = "view_submission",
            callback_id = "change_request_review",
            state_fixture = SWITCHER_STATE_SELECTION,
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'VALIDATED' })
def test_submit_for_review_group(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            req_type = "view_submission",
            callback_id = "change_request_review",
            state_fixture = GROUP_STATE_SELECTION,
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'IGNORED_ENVIRONMENT' })
def test_submit_without_approval_ignored(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            req_type = "view_submission",
            callback_id = "change_request_review",
            state_fixture = GROUP_STATE_SELECTION,
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', { 'message': 'Ticket validated', 'result': 'FROZEN_ENVIRONMENT' })
def test_submit_without_approval_frozen(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            req_type = "view_submission",
            callback_id = "change_request_review",
            state_fixture = GROUP_STATE_SELECTION,
            private_metadata = json.dumps({ 
                "domain_id": "1", "domain_name": "Test" 
            })
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {
        'channel_id': 'CHANNEL_ID',
        'channel': 'APPROVAL',
        'ticket': { '_id': 'ticket_123' }
    }, status = 201
)
def test_submit_request(client):
    private_metadata = json.dumps({
        "domain_id": "1", 
        "domain_name": "Test",
        "environment": DEFAULT_ENV,
        "environment_alias": PRODUCTION,
        "group": RELEASE_1,
        "switcher": MY_FEATURE1,
        "status": bool(True)
    })

    response = client.post(
        SLACK_EVENT, json = build_request_view(
            private_metadata = private_metadata,
            actions_fixture = build_static_select_action_value(
                action_id = "change_request_submit",
                text = "Submit"
            ),
            state_fixture = build_text_state_value(
                action_id = "selection_observation",
                value = OBSERVATION
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {
        'channel_id': 'CHANNEL_ID',
        'channel': 'APPROVAL',
        'ticket': { '_id': 'ticket_123' }
    }, status = 201
)
def test_submit_request_group(client):
    private_metadata = json.dumps({
        "domain_id": "1", 
        "domain_name": "Test",
        "environment": DEFAULT_ENV,
        "environment_alias": PRODUCTION,
        "group": RELEASE_1,
        "switcher": None,
        "status": bool(True)
    })

    response = client.post(
        SLACK_EVENT, json = build_request_view(
            private_metadata = private_metadata,
            actions_fixture = build_static_select_action_value(
                action_id = "change_request_submit",
                text = "Submit"
            ),
            state_fixture = build_text_state_value(
                action_id = "selection_observation",
                value = OBSERVATION
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {}, status = 400)
def test_submit_request_fail(client):
    private_metadata = json.dumps({
        "domain_id": "1", 
        "domain_name": "Test",
        "environment": DEFAULT_ENV,
        "environment_alias": PRODUCTION,
        "group": RELEASE_1,
        "switcher": MY_FEATURE1,
        "status": bool(True)
    })

    response = client.post(
        SLACK_EVENT, json = build_request_view(
            private_metadata = private_metadata,
            actions_fixture = build_static_select_action_value(
                action_id = "change_request_submit",
                text = "Submit"
            ),
            state_fixture = build_text_state_value(
                action_id = "selection_observation",
                value = OBSERVATION
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
def test_abort_request(client):
    response = client.post(
        SLACK_EVENT, json = build_request_view(
            actions_fixture = build_static_select_action_value(
                action_id = "change_request_abort",
                text = "Cancel"
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {'message': 'Ticket ticket123 processed'})
def test_approve_request(client):
    ticket_payload = {
      "id": "ticket123",
      "domain_id": "1",
    }

    response = client.post(
        SLACK_EVENT, json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_approved",
                text = "Approve",
                value = json.dumps(ticket_payload)
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {}, 400)
def test_approve_request_fail(client):
    ticket_payload = {
      "id": "ticket123",
      "domain_id": "1",
    }

    response = client.post(
        SLACK_EVENT, json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_approved",
                text = "Approve",
                value = json.dumps(ticket_payload)
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {'message': 'Ticker ticket123 processed'})
def test_deny_request(client):
    ticket_payload = {
      "id": "ticket123",
      "domain_id": "1",
    }

    response = client.post(
        SLACK_EVENT, json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_denied",
                text = "Deny",
                value = json.dumps(ticket_payload)
            )
        )
    )
    assert response.status_code == 200

@mock_event_handler
@mock_base_client(MODAL_REQUEST)
@mock_switcher_client('post', {}, 400)
def test_deny_request_fail(client):
    ticket_payload = {
      "id": "ticket123",
      "domain_id": "1",
    }

    response = client.post(
        SLACK_EVENT, json = build_request_message_view(
            actions_fixture = build_buttom_action_value(
                action_id = "request_denied",
                text = "Deny",
                value = json.dumps(ticket_payload)
            )
        )
    )
    assert response.status_code == 200
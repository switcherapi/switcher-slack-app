import json

from slack_sdk.errors import SlackApiError
from services.switcher_service import SwitcherService
from utils.switcher_util import get_keyval, validate_context_request
from utils.slack_payload_util import (
  populate_selection, 
  prepare_body, 
  get_state_salue,
  get_selected_action
)
from payloads.home import APP_HOME
from payloads.change_request import (
  create_request_review,
  create_block_message,
  get_request_message,
  read_request_metadata
)

def on_environment_selected(ack, body, client, logger):
  env_selected = get_selected_action(body)
  team_id = body["team"]["id"]

  ack()
  
  try:
    groups = SwitcherService().get_groups(team_id, env_selected)
    populate_selection(
      body = body["view"],
      item = "Group",
      values = get_keyval("name", groups)
    )

    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)

    client.views_update(
          view_id = view_id,
          hash = view_hash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting environment: {e}")

def on_group_selected(ack, body, client, view, logger):
  env_selected = get_state_salue(body["view"], "selection_environment")
  group_selected = get_selected_action(body)
  team_id = body["team"]["id"]

  ack()

  try:
    switchers = SwitcherService().get_switchers(
      team_id, env_selected, group_selected
    )
    populate_selection(
      body = body["view"],
      item = "Switcher",
      values = get_keyval("key", switchers)
    )

    populate_selection(body["view"], "Status", [
      { "name": "Enable", "value": "true" },
      { "name": "Disable", "value": "false" }
    ])

    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)
    client.views_update(
          view_id = view_id,
          hash = view_hash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting group: {e}")

def on_switcher_selected(ack, body, client, logger):
  ack()

  try:
    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)

    client.views_update(
          view_id = view_id,
          hash = view_hash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting switcher: {e}")

def on_change_request_review(ack, body, client, view, logger):
  user = body["user"]
  team_id = body["team"]["id"]

  ack()

  environment = get_state_salue(view, "selection_environment")
  context = {
    "environment": environment,
    "environment_alias": "Production" if environment == "default" else environment,
    "group": get_state_salue(view, "selection_group"),
    "switcher": get_state_salue(view, "selection_switcher"),
    "status": get_state_salue(view, "selection_status")
  }

  view = create_request_review(context)
  view["private_metadata"] = json.dumps(context)
  
  try:
    validate_context_request(context)
    SwitcherService().validate_ticket(team_id, context)
    
    # Request review
    client.views_publish(
      user_id = user["id"],
      view = view
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your request: {e}"
    )

def on_submit(ack, body, client, view, logger):
  user = body["user"]
  team_id = body["team"]["id"]

  ack()

  observation = get_state_salue(body["view"], "selection_observation")
  context = {
    **read_request_metadata(body["view"]),
    "observations": "" if observation is None else observation,
  }

  try:
    ticket = SwitcherService().create_ticket(team_id, context)

    # Return to initial state
    client.views_publish(
      response_action = "push",
      user_id = user["id"],
      view = APP_HOME
    )

    # Redirect approval
    client.chat_postMessage(
      channel = ticket.get("channel_id"),
      text = "The following request has been opened for approval.",
      blocks = get_request_message(ticket.get("ticket_id"), context)
    )
  except SlackApiError as e:
    message = e.response["error"]
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your submission: {message}"
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your request: {e}"
    )
  
def on_change_request_abort(ack, body, client, view, logger):
  ack()
  client.views_publish(
    response_action = "push",
    user_id = body["user"]["id"],
    view = APP_HOME
  )

def on_request_approved(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  ticket_id = body["actions"][0]["value"]
  channel_id = body["channel"]["id"]

  ack()

  message_blocks = create_block_message(":large_green_square: *Change request approved*")
  message_blocks.append(body["message"]["blocks"][2])

  try:
    SwitcherService().approve_request(team_id, ticket_id)
    client.chat_update(
      channel = channel_id,
      text = "Change request approved",
      ts = message_ts,
      blocks = message_blocks
    )
  except Exception as e:
    client.chat_update(
      channel = channel_id,
      text = e.args[0],
      ts = message_ts,
      blocks = create_block_message(f":large_yellow_square: *{e.args[0]}*")
    )

def on_request_denied(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  ticket_id = body["actions"][0]["value"]
  channel_id = body["channel"]["id"]

  ack()

  message_blocks = create_block_message(":large_red_square: *Change request denied*")
  message_blocks.append(body["message"]["blocks"][2])

  try:
    SwitcherService().deny_request(team_id, ticket_id)
    client.chat_update(
      channel = channel_id,
      text = "Change request denied",
      ts = message_ts,
      blocks = message_blocks
    )
  except Exception as e:
    client.chat_update(
      channel = channel_id,
      text = e.args[0],
      ts = message_ts,
      blocks = create_block_message(f":large_yellow_square: *{e.args[0]}*")
    )
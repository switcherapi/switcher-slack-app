import json

from payloads.home import APP_HOME
from utils.slack_payload_util import (
  populate_selection, 
  prepare_body, 
  get_state_salue,
  get_selected_action
)
from payloads.change_request import (
  create_request_review,
  create_block_message,
  get_request_message,
  read_request_metadata
)

from payloads import change_request

def on_environment_selected(ack, body, client, logger):
  env_selected = get_selected_action(body)
  
  populate_selection(body["view"], "Group", [
    { "name": "Release 1", "value": "Release 1" },
    { "name": "Release 2", "value": "Release 2" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepare_body(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting environment: {e}")

def on_group_selected(ack, body, client, view, logger):
  group_selected = get_selected_action(body)

  populate_selection(body["view"], "Switcher", [
    { "name": "MY_FEATURE1", "value": "MY_FEATURE1" },
    { "name": "MY_FEATURE2", "value": "MY_FEATURE2" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepare_body(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting group: {e}")

def on_switcher_selected(ack, body, client, logger):
  switcher_selected = get_selected_action(body)

  populate_selection(body["view"], "Status", [
    { "name": "Enable", "value": "true" },
    { "name": "Disable", "value": "false" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepare_body(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting switcher: {e}")

def on_change_request_review(ack, body, client, view):
  user = body["user"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]

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
    # Request review
    client.views_publish(
      user_id = user["id"],
      view = view
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your request"
    )

def on_submit(ack, body, client, view):
  user = body["user"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]

  ack()

  context = {
    **read_request_metadata(body["view"]),
    "observations": get_state_salue(body["view"], "selection_observation"),
  }

  try:
    # Return to initial state
    client.views_publish(
      response_action = "push",
      user_id = user["id"],
      view = APP_HOME
    )

    # Redirect approval
    client.chat_postMessage(
      channel = "C01SH298R6C",
      text = "The following request has been opened for approval.",
      blocks = get_request_message("ticket_123", context)
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your submission"
    )

def on_request_approved(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]
  ticket_id = body["actions"][0]["value"]

  ack()

  message_blocks = create_block_message(":large_green_square: *Change request approved*")
  message_blocks.append(body["message"]["blocks"][2])

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request approved",
    ts = message_ts,
    blocks = message_blocks
  )

def on_request_denied(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]
  ticket_id = body["actions"][0]["value"]

  ack()

  message_blocks = create_block_message(":large_red_square: *Change request denied*")
  message_blocks.append(body["message"]["blocks"][2])

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request denied",
    ts = message_ts,
    blocks = message_blocks
  )
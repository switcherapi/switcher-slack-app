import json

from payloads.home import APP_HOME
from utils.slack_payload_util import (
  populateSelection, 
  prepareBody, 
  getStateValue,
  getSelectedAction
)
from payloads.change_request import (
  createRequestReview,
  createBlockMessage,
  getRequestMessage,
  readRequestMetadata
)

from payloads import change_request

def onEnvironmentSelected(ack, body, client, logger):
  envSelected = getSelectedAction(body)
  
  populateSelection(body["view"], "Group", [
    { "name": "Release 1", "value": "Release 1" },
    { "name": "Release 2", "value": "Release 2" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepareBody(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting environment: {e}")

def onGroupSelected(ack, body, client, view, logger):
  groupSelected = getSelectedAction(body)

  populateSelection(body["view"], "Switcher", [
    { "name": "MY_FEATURE1", "value": "MY_FEATURE1" },
    { "name": "MY_FEATURE2", "value": "MY_FEATURE2" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepareBody(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting group: {e}")

def onSwitcherSelected(ack, body, client, logger):
  switcherSelected = getSelectedAction(body)

  populateSelection(body["view"], "Status", [
    { "name": "Enable", "value": "true" },
    { "name": "Disable", "value": "false" }
  ])

  viewHash = body["view"]["hash"]
  viewId = body["view"]["id"]

  prepareBody(body)

  try:
    ack()
    client.views_update(
          view_id = viewId,
          hash = viewHash,
          view = body["view"]
      )
  except Exception as e:
    logger.error(f"Error selecting switcher: {e}")

def onChangeRequestReview(ack, body, client, view):
  user = body["user"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]

  ack()

  environment = getStateValue(view, "selection_environment")
  context = {
    "environment": environment,
    "environment_alias": "Production" if environment == "default" else environment,
    "group": getStateValue(view, "selection_group"),
    "switcher": getStateValue(view, "selection_switcher"),
    "status": getStateValue(view, "selection_status")
  }

  view = createRequestReview(context)
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

def onSubmit(ack, body, client, view):
  user = body["user"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]

  ack()

  context = {
    **readRequestMetadata(body["view"]),
    "observations": getStateValue(body["view"], "selection_observation"),
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
      blocks = getRequestMessage("ticket_123", context)
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your submission"
    )

def onRequestApproved(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]
  ticketId = body["actions"][0]["value"]

  ack()

  messageBlocks = createBlockMessage(":large_green_square: *Change request approved*")
  messageBlocks.append(body["message"]["blocks"][2])

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request approved",
    ts = message_ts,
    blocks = messageBlocks
  )

def onRequestDenied(ack, body, client, logger):
  message_ts = body["message"]["ts"]
  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]
  ticketId = body["actions"][0]["value"]

  ack()

  messageBlocks = createBlockMessage(":large_red_square: *Change request denied*")
  messageBlocks.append(body["message"]["blocks"][2])

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request denied",
    ts = message_ts,
    blocks = messageBlocks
  )
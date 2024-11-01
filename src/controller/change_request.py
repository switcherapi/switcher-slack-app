import json

from slack_sdk.errors import SlackApiError
from services.switcher_service import SwitcherService
from utils.switcher_util import get_environment_keyval, get_keyval, validate_context_request
from utils.slack_payload_util import (
  populate_selection,
  populate_metadata,
  populate_selection_status,
  prepare_body, 
  get_status,
  get_state_value,
  get_state_name,
  get_selected_action,
  get_selected_action_text,
  get_selected_action_status
)
from payloads.home import APP_HOME
from payloads.change_request import NEW_SELECTION
from payloads.change_request import (
  create_request_review,
  create_block_message,
  get_request_message,
  read_request_metadata
)

def on_domain_selected(ack, body, client, logger):
  """ Load environments when domain is selected """

  ack()

  try:
    # Collect args
    team_id = body["team"]["id"]
    domain_id = get_selected_action(body)
    domain_name = get_selected_action_text(body)
    
    envs = SwitcherService().get_environments(team_id, domain_id)

    # Clear previous selection
    populate_selection(body["view"], "Group", NEW_SELECTION)
    populate_selection(body["view"], "Switcher", NEW_SELECTION)
    populate_selection(body["view"], "Status", NEW_SELECTION)

    # Populate view and metadata
    populate_selection(
      body = body["view"],
      item = "Environment",
      values = get_environment_keyval(envs)
    )

    populate_metadata(body["view"], { 
      "domain_id": domain_id,
      "domain_name": domain_name
    })

    # Push changes to view
    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)
    client.views_update(
      view_id = view_id,
      hash = view_hash,
      view = body["view"]
    )

    return body["view"]
  except Exception as e:
    error = f"Error opening change request form: {e}"
    logger.error(error)
    return error

def on_environment_selected(ack, body, client, logger):
  """ Load groups when environment is selected """

  ack()

  try:
    # Collect args
    env_selected = get_selected_action(body)
    team_id = body["team"]["id"]
    domain_id = read_request_metadata(body["view"])["domain_id"]

    groups = SwitcherService().get_groups(team_id, domain_id, env_selected)

    # Clear previous selection
    populate_selection(body["view"], "Group", NEW_SELECTION)
    populate_selection(body["view"], "Switcher", NEW_SELECTION)
    populate_selection(body["view"], "Status", NEW_SELECTION)

    # Populate view
    populate_selection(
      body = body["view"],
      item = "Group",
      values = get_keyval("name", groups)
    )
    
    # Push changes to view
    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)
    client.views_update(
      view_id = view_id,
      hash = view_hash,
      view = body["view"]
    )

    return body["view"]
  except Exception as e:
    error = f"Error selecting environment: {e}"
    logger.error(error)
    return error

def on_group_selected(ack, body, client, logger):
  """ Load switchers when group is selected """

  ack()

  try:
    # Collect args
    env_selected = get_state_value(body["view"], "selection_environment")
    group_selected = get_selected_action(body)
    group_status = get_selected_action_status(body)
    team_id = body["team"]["id"]
    domain_id = read_request_metadata(body["view"])["domain_id"]

    switchers = SwitcherService().get_switchers(
      team_id, domain_id, env_selected, group_selected
    )

    # Clear previous selection
    populate_selection(body["view"], "Switcher", NEW_SELECTION)

    # Populate view
    values = get_keyval("key", switchers)
    values.append({ "name": "-", "value": "-" })
    populate_selection(
      body = body["view"],
      item = "Switcher",
      values = values
    )

    populate_selection_status(body["view"], group_status)

    # Push changes to view
    view_hash = body["view"]["hash"]
    view_id = body["view"]["id"]

    prepare_body(body)
    client.views_update(
          view_id = view_id,
          hash = view_hash,
          view = body["view"]
      )

    return body["view"]
  except Exception as e:
    error = f"Error selecting group: {e}"
    logger.error(error)
    return error

def on_switcher_selected(ack, body, client):
  """ Updates view's metadata with switcher selection """

  ack()

  # Populate view
  selected_switcher = get_selected_action_text(body)
  if selected_switcher != "-":
    switcher_status = get_selected_action_status(body)
    populate_selection_status(body["view"], switcher_status)
  else:
    selected_group = get_state_name(body["view"], "selection_group")
    populate_selection_status(body["view"], get_status(selected_group))

  view_hash = body["view"]["hash"]
  view_id = body["view"]["id"]

  prepare_body(body)
  client.views_update(
      view_id = view_id,
      hash = view_hash,
      view = body["view"]
  )

  return body["view"]

def on_change_request_review(ack, body, client, view, logger):
  """ Populate context with selections, validate via Switcher API then publish view for review """

  ack()

  try:
    # Collect args
    user = body["user"]
    team_id = body["team"]["id"]
    environment = get_state_value(view, "selection_environment")

    # Create context and validate
    context = {
      **read_request_metadata(body["view"]),
      "environment": environment,
      "environment_alias": "Production" if environment == "default" else environment,
      "group": get_state_value(view, "selection_group"),
      "switcher": get_state_value(view, "selection_switcher"),
      "status": get_state_value(view, "selection_status")
    }

    validate_context_request(context)
    result = SwitcherService().validate_ticket(team_id, context)

    view = create_request_review(context)
    populate_metadata(view, context)

    # Publish view and send message
    user_message = None

    if result == 'VALIDATED':
      client.views_publish(
        user_id = user["id"],
        view = view
      )
    elif result == 'IGNORED_ENVIRONMENT':
      user_message = ":large_green_square: *Request does not require approval*: Updated with success!"
    elif result == 'FROZEN_ENVIRONMENT':
      user_message = ":large_red_square: *Request cannot be made*: Environment is frozen."
    
    if user_message is not None:
      client.chat_postMessage(
        channel = user["id"],
        text = "Change Request Review",
        blocks = create_block_message(user_message)
      )
    
    return view, user_message
  except Exception as e:
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your request: {e}"
    )

    error = f"Error on change request review: {e}"
    logger.error(error)
    return error

def on_submit(ack, body, client, logger):
  """ Create ticket, return to home view then publish approval message """

  ack()

  try:
    # Collect args
    observation = get_state_value(body["view"], "selection_observation")
    context = {
      **read_request_metadata(body["view"]),
      "observations": "" if observation is None else observation,
    }

    domain_id = context["domain_id"]
    user = body["user"]
    team_id = body["team"]["id"]

    # Return to initial state
    client.views_publish(
      response_action = "push",
      user_id = user["id"],
      view = APP_HOME
    )

    # Create ticket and post approval request
    ticket = SwitcherService().create_ticket(team_id, context)
    ticket_payload = {
      "id": ticket.get("ticket_id"),
      "domain_id": domain_id,
    }

    request_message = get_request_message(json.dumps(ticket_payload), context)
    client.chat_postMessage(
      channel = ticket.get("channel_id"),
      text = "The following request has been opened for approval.",
      blocks = request_message
    )

    return request_message, ticket
  except Exception as e:
    logger.error(f"Error on submitting: {e}")
    client.chat_postMessage(
      channel = user["id"], 
      text = f"There was an error with your request: {e}"
    )
  
def on_change_request_abort(ack, body, client):
  """ Return to home view """

  ack()

  client.views_publish(
    response_action = "push",
    user_id = body["user"]["id"],
    view = APP_HOME
  )

def on_request_approved(ack, body, client, logger):
  """ Approve ticket through Switcher API and update chat message """
  
  ack()

  try:
    # Collect args
    message_ts = body["message"]["ts"]
    team_id = body["team"]["id"]
    channel_id = body["channel"]["id"]

    ticket_payload = json.loads(body["actions"][0]["value"])
    domain_id = ticket_payload["domain_id"]
    ticket_id = ticket_payload["id"]

    message_blocks = create_block_message(":large_green_square: *Change request approved*")
    message_blocks.append(body["message"]["blocks"][2])

    # Approve ticket and update message
    SwitcherService().approve_request(team_id, domain_id, ticket_id)
    client.chat_update(
      channel = channel_id,
      text = "Change request approved",
      ts = message_ts,
      blocks = message_blocks
    )

    return message_blocks
  except Exception as e:
    logger.error(f"Error on aborting: {e}")
    client.chat_update(
      channel = channel_id,
      text = e.args[0],
      ts = message_ts,
      blocks = create_block_message(f":large_yellow_square: *{e.args[0]}*")
    )

def on_request_denied(ack, body, client, logger):
  """ Deny ticket through Switcher API and update chat message """
  
  ack()

  try:
    # Collect args
    message_ts = body["message"]["ts"]
    team_id = body["team"]["id"]
    channel_id = body["channel"]["id"]

    ticket_payload = json.loads(body["actions"][0]["value"])
    domain_id = ticket_payload["domain_id"]
    ticket_id = ticket_payload["id"]

    message_blocks = create_block_message(":large_red_square: *Change request denied*")
    message_blocks.append(body["message"]["blocks"][2])

    # Deny ticket and update message
    SwitcherService().deny_request(team_id, domain_id, ticket_id)
    client.chat_update(
      channel = channel_id,
      text = "Change request denied",
      ts = message_ts,
      blocks = message_blocks
    )
    
    return message_blocks
  except Exception as e:
    logger.error(f"Error on denying: {e}")
    client.chat_update(
      channel = channel_id,
      text = e.args[0],
      ts = message_ts,
      blocks = create_block_message(f":large_yellow_square: *{e.args[0]}*")
    )
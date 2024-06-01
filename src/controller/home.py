import copy

from services.switcher_service import SwitcherService
from payloads.home import MODAL_REQUEST, APP_HOME
from utils.slack_payload_util import populate_selection
from utils.switcher_util import get_keyval_of_keys

def on_home_opened(client, event, logger):
  """ Displays the home view """

  logger.warning(f"Home view opened by {event['user']}")
  client.views_publish(
    user_id = event["user"],
    view = APP_HOME
  )

  return APP_HOME

def on_change_request_opened(ack, body, client, logger):
  """ Displays the change request modal """

  ack()

  try:
    change_request = copy.deepcopy(MODAL_REQUEST)

    # Collect args
    team_id = body["team"]["id"]
    logger.warning(f"Team ID: {team_id}")

    domains = SwitcherService().get_domains(team_id)

    # Populate view
    populate_selection(
      body = change_request,
      item = "Domain",
      values = get_keyval_of_keys(["name", "id"], domains)
    )

    client.views_open(
      trigger_id = body["trigger_id"],
      view = change_request
    )

    return change_request
  except Exception as e:
    logger.error(f"Error opening change request form: {e}")
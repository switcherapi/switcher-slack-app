import copy

from services.switcher_service import SwitcherService
from payloads.home import MODAL_REQUEST, APP_HOME
from utils.slack_payload_util import populate_selection
from utils.switcher_util import get_environment_keyval

def on_home_opened(client, event, logger):
  """ Displays the home view """

  try:
    client.views_publish(
      user_id = event["user"],
      view = APP_HOME
    )

    return APP_HOME
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

def on_change_request_opened(ack, body, client, logger):
  """ Displays the change request modal """
  
  change_request = copy.deepcopy(MODAL_REQUEST)

  team_id = body["team"]["id"]
  logger.warning(f"Team ID: {team_id}")

  ack()

  try:
    switcher_service = SwitcherService()
    envs = switcher_service.get_environments(team_id)
    populate_selection(
      body = change_request,
      item = "Environment",
      values = get_environment_keyval(envs)
    )

    client.views_open(
      trigger_id = body["trigger_id"],
      view = change_request
    )

    return change_request
  except Exception as e:
    logger.error(f"Error opening change request form: {e}")
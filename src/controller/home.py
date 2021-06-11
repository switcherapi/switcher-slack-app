import copy

from utils.slack_payload_util import populate_selection
from payloads.home import MODAL_REQUEST, APP_HOME

def on_home_opened(client, event, logger):
  try:
    client.views_publish(
      user_id = event["user"],
      view = APP_HOME
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

def on_change_request_opened(ack, body, client, logger):
  change_request = copy.deepcopy(MODAL_REQUEST)

  team_id = body["team"]["id"]
  team_domain = body["team"]["domain"]
  logger.warning(f"Team ID: {team_id}")
  logger.warning(f"Team Domain: {team_domain}")

  ack()

  populate_selection(change_request, "Environment", [
    { "name": "Production", "value": "default" },
    { "name": "QA", "value": "QA" }
  ])

  try:
    client.views_open(
      trigger_id = body["trigger_id"],
      view = change_request
    )
  except Exception as e:
    logger.error(f"Error opening change request form: {e}")
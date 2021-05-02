import copy

from utils import populateSelection
from payloads.home import MODAL_REQUEST, APP_HOME

def onHomeOpened(client, event, logger):
  try:
    client.views_publish(
      user_id = event["user"],
      view = APP_HOME
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

def onChangeRequesOpened(ack, body, client, logger):
  change_request = copy.deepcopy(MODAL_REQUEST)

  populateSelection(change_request, "Environment", [
    { "name": "Production", "value": "default" },
    { "name": "QA", "value": "QA" }
  ])

  try:
    ack()
    client.views_open(
      trigger_id = body["trigger_id"],
      view = change_request
    )
  except Exception as e:
    logger.error(f"Error opening change request form: {e}")
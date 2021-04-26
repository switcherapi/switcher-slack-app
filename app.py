import os
import copy

from slack_bolt import App
from dotenv import load_dotenv
from utils.app_utils import populateSelection, prepareBody, getStateValue
from payloads.constants import MODAL_REQUEST, APP_HOME, REQUEST_SUBMISSION, REQUEST_SUBMISSION_BLOCKS

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Show the app landing page 
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
  try:
    client.views_publish(
      user_id = event["user"],
      view = APP_HOME
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

# Open Change Request modal
@app.action("request_change")
def open_change_request(ack, body, client, logger):
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

# Update Change Request modal with available domain groups
@app.action("selection_environment")
def selection_environment(ack, body, client, logger):
  envSelected = body["actions"][0]["selected_option"]["value"]
  print(f"Environment selected: {envSelected}")
  
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

# Update Change Request modal with available group switchers
@app.action("selection_group")
def selection_group(ack, body, client, view, logger):
  groupSelected = body["actions"][0]["selected_option"]["value"]
  print(f"Group selected: {groupSelected}")

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

# Update Change Request modal with status options
@app.action("selection_switcher")
def selection_switcher(ack, body, client, logger):
  switcherSelected = body["actions"][0]["selected_option"]["value"]
  print(f"Switcher selected: {switcherSelected}")

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

# Confirm status selection
@app.action("selection_status")
def selection_status(ack, body, client, logger):
  ack()

# Submit Change Request for verification and approval
@app.view("change_request_view")
def handle_submission(ack, body, client, view):
  user = body["user"]
  ack()

  optionEnv = getStateValue(view, "selection_environment")
  optionGroup = getStateValue(view, "selection_group")
  optionSwitcher = getStateValue(view, "selection_switcher")
  optionStatus = getStateValue(view, "selection_status")
  optionObs = getStateValue(view, "selection_observation")

  msg = ""
  try:
    msg = f"{user['name']}, your request was successfully sent"
  except Exception as e:
    msg = "There was an error with your submission"
  finally:
    # Request preview
    client.views_publish(
      response_action = "push",
      user_id = user["id"],
      view = REQUEST_SUBMISSION
    )

    # Redirect approval
    client.chat_postMessage(
      channel = "C01SH298R6C",
      blocks = REQUEST_SUBMISSION_BLOCKS
    )

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
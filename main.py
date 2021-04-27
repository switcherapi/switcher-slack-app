import os
import copy

from slack_bolt import App
from dotenv import load_dotenv
from util.utils import (
  populateSelection, 
  prepareBody, 
  getStateValue,
  addField,
  addSummary,
  addHeaderValue,
)
from payloads.constants import (
  MODAL_REQUEST, 
  APP_HOME, REQUEST_SUMMARY, 
  REQUEST_MESSAGE
)

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
  print(body)
  user = body["user"]
  ack()

  optionEnv = getStateValue(view, "selection_environment")
  optionGroup = getStateValue(view, "selection_group")
  optionSwitcher = getStateValue(view, "selection_switcher")
  optionStatus = getStateValue(view, "selection_status")
  optionObs = getStateValue(view, "selection_observation")

  summary = copy.deepcopy(REQUEST_SUMMARY)
  addSummary(summary["blocks"], "Environment", optionEnv)
  addSummary(summary["blocks"], "Group", optionGroup)
  addSummary(summary["blocks"], "Switcher", optionSwitcher)
  addSummary(summary["blocks"], "Status", optionStatus)
  addHeaderValue(summary["blocks"], "Observations", optionObs)

  message = copy.deepcopy(REQUEST_MESSAGE)
  addField(message[1]["fields"], "Environment", optionEnv)
  addField(message[1]["fields"], "Group", optionGroup)
  addField(message[1]["fields"], "Switcher", optionSwitcher)
  addField(message[1]["fields"], "Status", optionStatus)
  addField(message[1]["fields"], "Observations", optionObs)

  try:
    # Request preview
    client.views_publish(
      response_action = "push",
      user_id = user["id"],
      view = summary
    )

    # Redirect approval
    client.chat_postMessage(
      channel = "C01SH298R6C",
      text = "The following request has been opened for approval.",
      blocks = message
    )
  except Exception as e:
    client.chat_postMessage(
      channel = user, 
      text = "There was an error with your submission"
    )

# Request approved
@app.action("request_approved")
def request_approved(ack, body, client):
  message_ts = body["message"]["ts"]
  ack()

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request approved",
    ts = message_ts,
    blocks = [
      {
          "type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "Change request approved."
          }
      }]
  )

# Request denied
@app.action("request_denied")
def request_denied(ack, body, client, logger):
  ack()

  client.chat_update(
    channel = "C01SH298R6C",
    text = "Change request denied",
    ts = message_ts,
    blocks = [
      {
          "type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "Change request denied."
          }
      }]
  )

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
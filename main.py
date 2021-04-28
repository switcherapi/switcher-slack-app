import os

from slack_bolt import App
from dotenv import load_dotenv
from controller.home import onChangeRequesOpened, onHomeOpened
from controller.change_request import (
  onEnvironmentSelected,
  onGroupSelected,
  onSwitcherSelected,
  onStatusSelected,
  onSubmit,
  onRequestApproved,
  onRequestDenied
)

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Show the app landing page 
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
  onHomeOpened(client, event, logger)

# Open Change Request modal
@app.action("request_change")
def open_change_request(ack, body, client, logger):
  onChangeRequesOpened(ack, body, client, logger)

# Update Change Request modal with available domain groups
@app.action("selection_environment")
def selection_environment(ack, body, client, logger):
  onEnvironmentSelected(ack, body, client, logger)
  
# Update Change Request modal with available group switchers
@app.action("selection_group")
def selection_group(ack, body, client, view, logger):
  onGroupSelected(ack, body, client, view, logger)

# Update Change Request modal with status options
@app.action("selection_switcher")
def selection_switcher(ack, body, client, logger):
  onSwitcherSelected(ack, body, client, logger)

# Confirm status selection
@app.action("selection_status")
def selection_status(ack, body, client, logger):
  onStatusSelected(ack, body, client, logger)

# Submit Change Request for verification and approval
@app.view("change_request_view")
def handle_submission(ack, body, client, view):
  onSubmit(ack, body, client, view)

# Request approved
@app.action("request_approved")
def request_approved(ack, body, client, logger):
  onRequestApproved(ack, body, client, logger)

# Request denied
@app.action("request_denied")
def request_denied(ack, body, client, logger):
  onRequestDenied(ack, body, client, logger)

if __name__ == "__main__":
    app.start(port = int(os.environ.get("PORT", 3000)))
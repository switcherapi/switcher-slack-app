import os

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse

from dotenv import load_dotenv

from services.switcher_store import SwitcherInstallationStoreService
from store import SwitcherAppInstallationStore
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
switcher_url = os.environ.get("SWITCHER_URL")

def success(args: SuccessArgs) -> BoltResponse:
  assert args.request is not None
  t = args.installation.bot_token
  ch = args.installation.incoming_webhook_channel
  chid = args.installation.incoming_webhook_channel_id

  return BoltResponse(
    status = 308,
    headers = {
      "Location": f"{switcher_url}/?t={t}&ch={ch}&chid={chid}",
    },
    body = ""
  )

def failure(args: FailureArgs) -> BoltResponse:
  assert args.request is not None
  assert args.reason is not None
  return BoltResponse(
    status = 308,
    headers = {
      "Location": f"{switcher_url}/documentation",
    },
    body = ""
  )

app = App(
  signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
  installation_store = SwitcherAppInstallationStore(base_dir="./data"),
  oauth_settings = OAuthSettings(
    client_id = os.environ.get("SLACK_CLIENT_ID"),
    client_secret = os.environ.get("SLACK_CLIENT_SECRET"),
    scopes = ["chat:write", "commands", "incoming-webhook"],
    user_scopes = ["im:history"],
    redirect_uri = None,
    install_path = "/slack/install",
    redirect_uri_path = "/slack/oauth_redirect",
    state_store = FileOAuthStateStore(expiration_seconds=600, base_dir="./data"),
    callback_options = CallbackOptions(success=success, failure=failure)
  )
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

from flask import Flask, request, session, make_response
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Handles requests from Slack API server
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
  return handler.handle(request)

# Starts Slack OAuth (=app installation) flow
@flask_app.route("/slack/install", methods=["GET"])
def install():
  return handler.handle(request)

# Handles the redirection from Slack's OAuth flow
@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
  return handler.handle(request)


##### Testing resource #####
import json
switcher_services = SwitcherInstallationStoreService()

@flask_app.route("/switcher_api/saveinstallation", methods=["POST"])
def saveinstallation():
  installation_filepath = "./data/TUUUUUUU/installer-latest"
  bot_filepath = "./data/TUUUUUUU/bot-latest"

  with open(installation_filepath) as f:
    inst_payload = json.loads(f.read())

  with open(bot_filepath) as f:
    bot_payload = json.loads(f.read())

  return switcher_services.save_installation(
    enterprise_id = None,
    team_id = "TUUUUUUU", 
    user_id = "UUUUUUUU",
    installation_payload = inst_payload,
    bot_payload = bot_payload
  )

@flask_app.route("/switcher_api/findbot", methods=["GET"])
def findbot():
  return switcher_services.find_bot(
    enterprise_id = None,
    team_id = "TUUUUUUU"
  )

@flask_app.route("/switcher_api/findinstallation", methods=["GET"])
def findinstallation():
  return switcher_services.find_installation(
    enterprise_id = None,
    team_id = "TUUUUUUU"
  )

if __name__ == "__main__":
  flask_app.run()
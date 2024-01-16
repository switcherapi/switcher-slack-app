import os
import logging

from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.state_store import FileOAuthStateStore

from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse

from store.switcher_store import SwitcherAppInstallationStore
from controller.home import on_change_request_opened, on_home_opened
from controller.change_request import (
  on_environment_selected,
  on_group_selected,
  on_switcher_selected,
  on_change_request_review,
  on_submit,
  on_change_request_abort,
  on_request_approved,
  on_request_denied
)

load_dotenv()
switcher_url = os.environ.get("SWITCHER_URL")
switcher_api_url = os.environ.get("SWITCHER_API_URL")
release_time = os.environ.get("RELEASE_TIME", "latest")
version = f"1.0.6 {release_time}"
# logging.basicConfig(level = logging.WARNING)

def success(args: SuccessArgs) -> BoltResponse:
  assert args.request is not None
  t_id = args.installation.team_id
  e_id = args.installation.enterprise_id

  if e_id is None: e_id = ""
  if t_id is None: t_id = ""

  return BoltResponse(
    status = 308,
    headers = {
      "Location": f"{switcher_url}/slack/authorization?e_id={e_id}&t_id={t_id}",
    }
  )

def failure(args: FailureArgs) -> BoltResponse:
  assert args.request is not None
  assert args.reason is not None

  return BoltResponse(
    status = 308,
    headers = {
      "Location": f"{switcher_url}/slack/authorization?error=1&reason={args.reason}",
    }
  )

app = App(
  signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
  installation_store = SwitcherAppInstallationStore(),
  oauth_settings = OAuthSettings(
    client_id = os.environ.get("SLACK_CLIENT_ID"),
    client_secret = os.environ.get("SLACK_CLIENT_SECRET"),
    scopes = ["chat:write", "commands", "incoming-webhook"],
    user_scopes = ["im:history"],
    redirect_uri = None,
    install_path = "/slack/install",
    redirect_uri_path = "/slack/oauth_redirect",
    state_store = FileOAuthStateStore(expiration_seconds = 600, base_dir = "./data"),
    callback_options = CallbackOptions(success = success, failure = failure)
  )
)

# Show the app landing page 
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
  on_home_opened(client, event, logger)

# Open Change Request modal
@app.action("change_request")
def open_change_request(ack, body, client, logger):
  on_change_request_opened(ack, body, client, logger)

# Update Change Request modal with available domain groups
@app.action("selection_environment")
def selection_environment(ack, body, client, logger):
  on_environment_selected(ack, body, client, logger)
  
# Update Change Request modal with available group switchers
@app.action("selection_group")
def selection_group(ack, body, client, view, logger):
  on_group_selected(ack, body, client, logger)

# Update Change Request modal with status options
@app.action("selection_switcher")
def selection_switcher(ack, body, client, logger):
  on_switcher_selected(ack, body, client)

# Confirm status selection
@app.action("selection_status")
def selection_status(ack, body, client, logger):
  ack()

# Submit Change Request for review
@app.view("change_request_review")
def handle_change_request_review(ack, body, client, view, logger):
  on_change_request_review(ack, body, client, view, logger)

# Submit Change Request for verification and approval
@app.action("change_request_submit")
def handle_submission(ack, body, client, view, logger):
  on_submit(ack, body, client, logger)

# Abort Change Request
@app.action("change_request_abort")
def handle_change_request_abort(ack, body, client, view, logger):
  on_change_request_abort(ack, body, client)

# Request approved
@app.action("request_approved")
def request_approved(ack, body, client, logger):
  on_request_approved(ack, body, client, logger)

# Request denied
@app.action("request_denied")
def request_denied(ack, body, client, logger):
  on_request_denied(ack, body, client, logger)

from flask import Flask, request, session, make_response
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Health check
@flask_app.route("/check", methods = ["GET"])
def health_check():
  return {
    "status": "UP",
    "version": version,
    "switcher_cloud": switcher_url,
    "switcher_api": switcher_api_url
  }

# Handles requests from Slack API server
@flask_app.route("/slack/events", methods = ["POST"])
def slack_events():
  return handler.handle(request)

# Starts Slack OAuth (=app installation) flow
@flask_app.route("/slack/install", methods = ["GET"])
def slack_install():
  return handler.handle(request)

# Handles the redirection from Slack's OAuth flow
@flask_app.route("/slack/oauth_redirect", methods = ["GET"])
def oauth_redirect():
  return handler.handle(request)

if __name__ == "__main__":
  flask_app.run()
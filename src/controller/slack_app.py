import os

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk.oauth.state_store import FileOAuthStateStore

from flask import Flask, request, session, make_response

from utils.constants import SWITCHER_URL, SWITCHER_API_URL, VERSION
from store.switcher_store import SwitcherAppInstallationStore
        
class SlackAppHandler:
    def build_app(self, api_url: str = os.environ.get("SWITCHER_API_URL")):
        """ Build the Slack App Settings """
        
        return App(
            signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
            installation_store = SwitcherAppInstallationStore(api_url),
            oauth_settings = OAuthSettings(
                client_id = os.environ.get("SLACK_CLIENT_ID"),
                client_secret = os.environ.get("SLACK_CLIENT_SECRET"),
                scopes = ["chat:write", "commands", "incoming-webhook"],
                user_scopes = ["im:history"],
                redirect_uri = None,
                install_path = "/slack/install",
                redirect_uri_path = "/slack/oauth_redirect",
                state_store = FileOAuthStateStore(expiration_seconds = 600, base_dir = "./data"),
                callback_options = CallbackOptions(success = self.success, failure = self.failure)
            )
        )

    def register_handler(self, app):
        """ Register the Slack App handler """

        flask_app = Flask(__name__)
        handler = SlackRequestHandler(app)

        # Health check
        @flask_app.route("/check", methods = ["GET"])
        def health_check():
            return {
                "status": "UP",
                "version": VERSION,
                "switcher_cloud": SWITCHER_URL,
                "switcher_api": SWITCHER_API_URL
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

        return flask_app

    def success(self, args: SuccessArgs) -> BoltResponse:
        assert args.request is not None
        t_id = args.installation.team_id
        e_id = args.installation.enterprise_id

        if e_id is None: e_id = ""
        if t_id is None: t_id = ""

        return BoltResponse(
            status = 308,
            headers = {
                "Location": f"{SWITCHER_URL}/slack/authorization?e_id={e_id}&t_id={t_id}",
            }
        )

    def failure(self, args: FailureArgs) -> BoltResponse:
        assert args.request is not None
        assert args.reason is not None

        return BoltResponse(
            status = 308,
            headers = {
                "Location": f"{SWITCHER_URL}/slack/authorization?error=1&reason={args.reason}",
            }
        )
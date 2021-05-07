from slack_sdk.web import SlackResponse

OPEN_APP_HOME_FIX1 = {
   "token": "token",
   "team_id": "team_id",
   "api_app_id": "api_app_id",
   "event": {
      "type": "app_home_opened",
      "user": "user",
      "channel": "channel",
      "tab": "home",
      "view": {},
      "event_ts": "1620322783.186629"
   },
   "type": "event_callback",
   "event_id": "event_id",
   "event_time": 1620322783,
   "authorizations": [
      {
         "enterprise_id": "None",
         "team_id": "team_id",
         "user_id": "user_id",
         "is_bot": bool(True),
         "is_enterprise_install": bool(False)
      }
   ],
   "is_ext_shared_channel": bool(False)
}

ACTION_OPEN_MODAL_CHANGE_REQUEST_FIX1 = {
   "action_id": "request_change",
   "block_id": "lGG",
   "text": {
      "type": "plain_text",
      "text": "Request Change"
   },
   "value": "test",
   "type": "button",
   "action_ts": "1620361208.200121"
}

def build_action_value(action_id: str, text: str, value = None):
   return {
      "type": "static_select",
      "action_id": action_id,
      "block_id": "w4M1",
      "selected_option": {
         "text": {
            "type": "plain_text",
            "text": text
         },
         "value": value
      },
      "placeholder": {
         "type": "plain_text",
         "text": "Select an item"
      }
   }

def build_state_value(action_id: str, text: str, value: str):
   return {
      "values": {
         "w4M1": {
            "selection_group": {
               "type": "static_select",
               action_id: {
                  "text": {
                     "type": "plain_text",
                     "text": text
                  },
                  "value": value
               }
            }
         }
      }
   }


def build_request_view(
   actions_fixture: dict,
   state_fixture: dict = {}
):
   """ Create a change request input based on the action fixture """
   return {
      "type": "block_actions",
      "user": {
         "id": "user_id",
         "username": "username",
         "name": "user",
         "team_id": "team_id"
      },
      "api_app_id": "api_app_id",
      "token": "token",
      "trigger_id": "trigger_id",
      "team": {
         "id": "team_id",
         "domain": "domain"
      },
      "enterprise": "",
      "is_enterprise_install": bool(False),
      "view": {
         "id": "view_id",
         "team_id": "team_id",
         "type": "modal",
         "blocks": [],
         "private_metadata": "",
         "callback_id": "change_request_view",
         "state": state_fixture,
         "hash": "hash",
         "title": {
            "type": "plain_text",
            "text": "Switcher Change Request"
         },
         "previous_view_id": "",
         "root_view_id": "root_view_id",
         "app_id": "app_id",
         "external_id": "",
         "app_installed_team_id": "app_installed_team_id",
         "bot_id": "bot_id"
      },
      "actions": [actions_fixture]
   }


def get_slack_events_response(
    req_args: dict,
    data: dict,
    status_code: int = 200
) -> SlackResponse:
    return SlackResponse(
        client = None,
        http_verb = "POST",
        api_url = "/slack/events",
        req_args = {
            "json": {
                "view": req_args
            }
        },
        data = {
            "ok": bool(True),
            "view": data
        },
        headers = {
            "content-type": "application/json; charset=utf-8",
            "x-oauth-scopes": "chat:write,commands,incoming-webhook",
            "access-control-allow-origin": "*",
            "x-slack-req-id": "x-slack-req-id"
        },
        status_code = status_code,
    )
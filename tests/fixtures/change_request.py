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

OPEN_MODAL_CHANGE_REQUEST_FIX1 = {
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
   "view": {},
   "actions": [
      {
         "action_id": "request_change",
         "block_id": "lGG",
         "text": {
            "type": "plain_text",
            "text": "Request Change",
            "emoji": bool(True)
         },
         "value": "test",
         "type": "button",
         "action_ts": "1620361208.200121"
      }
   ]
}

ENVIRONMENT_SELECTION_FIX1 = {
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
      "id": "V0216F9BP9Q",
      "team_id": "TUW2RH760",
      "type": "modal",
      "blocks": [],
      "private_metadata": "",
      "callback_id": "change_request_view",
      "state": {
         "values": {
            "w4M1": {
               "selection_environment": {
                  "type": "static_select",
                  "selected_option": {
                     "text": {
                        "type": "plain_text",
                        "text": "Production",
                        "emoji": bool(True)
                     },
                     "value": "default"
                  }
               }
            },
            "qZyOs": {
               "selection_group": {
                  "type": "static_select",
                  "selected_option": ""
               }
            },
            "EKV": {
               "selection_switcher": {
                  "type": "static_select",
                  "selected_option": ""
               }
            },
            "e0gs": {
               "selection_status": {
                  "type": "static_select",
                  "selected_option": ""
               }
            },
            "iedYD": {
               "selection_observation": {
                  "type": "plain_text_input",
                  "value": ""
               }
            }
         }
      },
      "hash": "1620362173.OoxEmivF",
      "title": {
         "type": "plain_text",
         "text": "Switcher Change Request",
         "emoji": bool(True)
      },
      "clear_on_close": bool(False),
      "notify_on_close": bool(False),
      "close": {
         "type": "plain_text",
         "text": "Cancel",
         "emoji": bool(True)
      },
      "submit": {
         "type": "plain_text",
         "text": "Submit",
         "emoji": bool(True)
      },
      "previous_view_id": "",
      "root_view_id": "root_view_id",
      "app_id": "app_id",
      "external_id": "",
      "app_installed_team_id": "app_installed_team_id",
      "bot_id": "bot_id"
   },
   "actions": [
      {
         "type": "static_select",
         "action_id": "selection_environment",
         "block_id": "w4M1",
         "selected_option": {
            "text": {
               "type": "plain_text",
               "text": "Production",
               "emoji": bool(True)
            },
            "value": "default"
         },
         "placeholder": {
            "type": "plain_text",
            "text": "Select an item",
            "emoji": bool(True)
         },
         "action_ts": "1620362181.104763"
      }
   ]
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
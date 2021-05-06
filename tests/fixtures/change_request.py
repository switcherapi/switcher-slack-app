from slack_sdk.web import SlackResponse

OPEN_CHANGE_REQUEST_MODAL_FIX1 = {
   "token": "token",
   "team_id": "team_id",
   "api_app_id": "api_app_id",
   "event": {
      "type": "app_home_opened",
      "user": "user",
      "channel": "channel",
      "tab": "home",
      "view": {
         "id": "V021UFM1N6L",
         "team_id": "team_id",
         "type": "home",
         "blocks": [
            {
               "type": "context",
               "block_id": "hrp",
               "elements": [
                  {
                     "type": "plain_text",
                     "text": "What are you up today?",
                     "emoji": bool(True)
                  }
               ]
            },
            {
               "type": "divider",
               "block_id": "iNu"
            },
            {
               "type": "actions",
               "block_id": "G1c",
               "elements": [
                  {
                     "type": "button",
                     "action_id": "request_change",
                     "text": {
                        "type": "plain_text",
                        "text": "Request Change",
                        "emoji": bool(True)
                     }
                  }
               ]
            }
         ],
         "private_metadata": "",
         "callback_id": "",
         "state": {
            "values": {
               
            }
         },
         "hash": "1620322317.W2kv14tJ",
         "title": {
            "type": "plain_text",
            "text": "View Title",
            "emoji": bool(True)
         },
         "clear_on_close": bool(False),
         "notify_on_close": bool(False),
         "close": "None",
         "submit": "None",
         "previous_view_id": "None",
         "root_view_id": "root_view_id",
         "app_id": "app_id",
         "external_id": "",
         "app_installed_team_id": "app_installed_team_id",
         "bot_id": "bot_id"
      },
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
app_home_opened_payload = {
    "type": "home",
    "callback_id": "home_view",
    "blocks": [
        {
            "type": "section",
            "text": {
            "type": "mrkdwn",
            "text": "Welcome to Switcher API App"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
            "type": "mrkdwn",
            "text": "Press the button to save a turtle."
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                    "type": "plain_text",
                    "text": "Save"
                    }
                }
            ]
        }
    ]
}
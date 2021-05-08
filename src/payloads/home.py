MODAL_REQUEST = {
	"callback_id": "change_request_review",
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "Switcher Change Request"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel"
	},
	"blocks": [
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Select the options below to request a Switcher status change."
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Environment"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item"
				},
				"options": [],
				"action_id": "selection_environment"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Group"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "-"
						},
						"value": "-"
					}
				],
				"action_id": "selection_group"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Switcher"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "-"
						},
						"value": "-"
					}
				],
				"action_id": "selection_switcher"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Status"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "-"
						},
						"value": "-"
					}
				],
				"action_id": "selection_status"
			}
		}
	]
}

APP_HOME = {
	"type": "home",
	"blocks": [
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "What are you up today?"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Request Change"
					},
					"action_id": "request_change"
				}
			]
		}
	]
}
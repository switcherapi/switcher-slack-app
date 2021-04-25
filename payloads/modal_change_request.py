modal_change_request = {
	"callback_id": "change_request_view",
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
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Production"
						},
						"value": "default"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Development"
						},
						"value": "Development"
					}
				],
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
							"text": "Release 1"
						},
						"value": "Release 1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Release 2"
						},
						"value": "Release 2"
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
							"text": "MY_FEATURE01"
						},
						"value": "MY_FEATURE01"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "MY_FEATURE02"
						},
						"value": "MY_FEATURE02"
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
							"text": "Activate"
						},
						"value": "true"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Deactivate"
						},
						"value": "false"
					}
				],
				"action_id": "selection_status"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": bool("true"),
				"action_id": "selection_observation"
			},
			"label": {
				"type": "plain_text",
				"text": "Observations"
			}
		}
	]
}
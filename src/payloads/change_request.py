import copy
import json

from utils.slack_payload_util import (
  add_field,
  insert_summary,
  insert_summary_value
)

NEW_SELECTION = [{ "name": "-", "value": "-" }]

REQUEST_REVIEW = {
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Change Request Review"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Please, review your request and submit it for approval."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": bool(True),
				"action_id": "selection_observation"
			},
			"label": {
				"type": "plain_text",
				"text": "Observations"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit"
					},
					"style": "primary",
					"action_id": "change_request_submit"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Cancel"
					},
					"style": "danger",
					"action_id": "change_request_abort"
				}
			]
		}
	]
}

def create_block_message(text):
	return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		},
		{
			"type": "divider"
		}
	]

def get_request_message(ticket_payload, context):
	message = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "The following request has been opened for approval"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": []
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Approve"
					},
					"style": "primary",
					"value": ticket_payload,
					"action_id": "request_approved"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Deny"
					},
					"style": "danger",
					"value": ticket_payload,
					"action_id": "request_denied"
				}
			]
		}
	]

	add_field(message[2]["fields"], "Domain", context["domain_name"])
	add_field(message[2]["fields"], "Environment", context["environment"])
	add_field(message[2]["fields"], "Group", context["group"])
	if context["switcher"] is not None:
		add_field(message[2]["fields"], "Switcher", context["switcher"])

	add_field(message[2]["fields"], "Status", "Enable" if context["status"] == "true" else "Disable")
	add_field(message[2]["fields"], "Observations", context.get("observations", ""))
	return message

def create_request_review(context):
	view = copy.deepcopy(REQUEST_REVIEW)
	insert_summary(view["blocks"], 3, "Domain", context["domain_name"])
	insert_summary(view["blocks"], 4, "Environment", context["environment"])
	insert_summary(view["blocks"], 5, "Group", context["group"])

	status = "Enable" if context["status"] == "true" else "Disable"
	if context["switcher"] is not None:
		insert_summary(view["blocks"], 6, "Switcher", context["switcher"])
		insert_summary_value(view["blocks"], 7, status)
	else:
		insert_summary_value(view["blocks"], 6, status)
	
	return view

def read_request_metadata(view):
	return json.loads(view.get("private_metadata", {}))

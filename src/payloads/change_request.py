import copy
import json

from utils.slack_payload_util import (
  addField,
  addSummary,
  insertSummary,
  addHeaderValue,
)

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

def createBlockMessage(text):
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

def getRequestMessage(ticketId, context):
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
					"value": ticketId,
					"action_id": "request_approved"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Deny"
					},
					"style": "danger",
					"value": ticketId,
					"action_id": "request_denied"
				}
			]
		}
	]

	addField(message[2]["fields"], "Environment", context["environment"])
	addField(message[2]["fields"], "Group", context["group"])
	addField(message[2]["fields"], "Switcher", context["switcher"])
	addField(message[2]["fields"], "Status", "Enable" if bool(context["status"]) else "Disable")
	addField(message[2]["fields"], "Observations", context["observations"])
	return message

def createRequestReview(context):
	view = copy.deepcopy(REQUEST_REVIEW)
	insertSummary(view["blocks"], 3, "Environment", context["environment"])
	insertSummary(view["blocks"], 4, "Group", context["group"])
	insertSummary(view["blocks"], 5, "Switcher", context["switcher"])
	insertSummary(view["blocks"], 6, "Status", "Enable" if bool(context["status"]) else "Disable")
	return view

def readRequestMetadata(view):
	metadata = view.get("private_metadata", None)
	if metadata is not None:
		return json.loads(metadata)
	return {}

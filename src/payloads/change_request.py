import copy
from utils import (
  addField,
  addSummary,
  addHeaderValue,
)

REQUEST_SUMMARY = {
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Change Request Submitted"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "The following request has been opened for approval."
			}
		},
		{
			"type": "divider"
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

def createSummary(context):
	summary = copy.deepcopy(REQUEST_SUMMARY)
	addSummary(summary["blocks"], "Environment", context["environment"])
	addSummary(summary["blocks"], "Group", context["group"])
	addSummary(summary["blocks"], "Switcher", context["switcher"])
	addSummary(summary["blocks"], "Status", "Enable" if bool(context["status"]) else "Disable")
	addHeaderValue(summary["blocks"], "Observations", context["observations"])
	return summary
def populateSelection(body, item, values):
    """Includes values to selection block"""
    for block in body["blocks"]:
        text = block.get("text", {})
        if text.get("text", None) == item:
            block["accessory"]["options"] = []
            for value in values:
                block["accessory"]["options"].append({
                    "text": {
                        "type": "plain_text",
                        "text": value["name"]
                    },
                    "value": value["value"]
                })
            return block

def addSummary(block, label, value):
    """Add custom header (label) body (value) to block"""
    block.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"```{label}```\n> {value}"
			}
		})

def insertSummary(block, index, label, value):
    """Add label and value to block"""
    block.insert(index, {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"```{label}```\n> {value}"
			}
		})

def addField(fields, label, value):
    fields.append({
            "type": "mrkdwn",
            "text": f"*{label}:*\n{value}"
        })

def addHeaderValue(block, label, value):
    """Add bold header title followed by plain text"""
    block.append({
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": label
			}
		})

    block.append({
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": value
			}
		})

def prepareBody(body):
    """Prepare view to be forwarded"""
    body["view"].pop("id")
    body["view"].pop("team_id")
    body["view"].pop("state")
    body["view"].pop("hash")
    body["view"].pop("previous_view_id")
    body["view"].pop("root_view_id")
    body["view"].pop("app_id")
    body["view"].pop("app_installed_team_id")
    body["view"].pop("bot_id")

def getStateValue(view, option):
    """Get selected values stored at the state element"""
    elementValue = ""
    for element in view["state"]["values"]:
        elementValue = view["state"]["values"][element].get(option, None)
        if elementValue is not None:
            if elementValue.get("selected_option", None) is not None:
                return elementValue["selected_option"]["value"]
            return elementValue.get("value", None)

def getSelectedAction(body):
    """Get selected value from an action event"""
    if body["actions"] is not None and len(body["actions"]) > 0:
        return body["actions"][0]["selected_option"]["value"]
    return ""
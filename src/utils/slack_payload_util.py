def populate_selection(body, item, values):
    """ Includes values to selection block """

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

def insert_summary(block, index, label, value):
    """ Add label and value to block """

    block.insert(index, {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"```{label}```\n> {value}"
			}
		})

def add_field(fields, label, value):
    fields.append({
            "type": "mrkdwn",
            "text": f"*{label}:*\n{value}"
        })

def prepare_body(body):
    """ Prepare view to be forwarded """

    body["view"].pop("id")
    body["view"].pop("team_id")
    body["view"].pop("state")
    body["view"].pop("hash")
    body["view"].pop("previous_view_id")
    body["view"].pop("root_view_id")
    body["view"].pop("app_id")
    body["view"].pop("app_installed_team_id")
    body["view"].pop("bot_id")

def get_state_value(view, option):
    """ Get selected values stored at the state element """

    element_value = ""
    for element in view["state"]["values"]:
        element_value = view["state"]["values"][element].get(option, None)
        if element_value is not None:
            if element_value.get("selected_option", None) is not None:
                return element_value["selected_option"]["value"]
            return element_value.get("value", None)

def get_selected_action(body):
    """ Get selected value from an action event """
    
    if body["actions"] is not None and len(body["actions"]) > 0:
        return body["actions"][0]["selected_option"]["value"]
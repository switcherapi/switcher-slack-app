# Includes values to selection block
def populateSelection(body, item, values):
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

# Prepare view to be forwarded 
def prepareBody(body):
    body["view"].pop("id")
    body["view"].pop("team_id")
    body["view"].pop("state")
    body["view"].pop("hash")
    body["view"].pop("previous_view_id")
    body["view"].pop("root_view_id")
    body["view"].pop("app_id")
    body["view"].pop("app_installed_team_id")
    body["view"].pop("bot_id")

# Get selected values stored at the state element
def getStateValue(view, option):
    elementValue = ""
    for element in view["state"]["values"]:
        elementValue = view["state"]["values"][element].get(option, None)
        if not (elementValue is None):
            if not (elementValue.get("selected_option", None) is None):
                return elementValue["selected_option"]["value"]
            return elementValue["value"]
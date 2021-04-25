import os
from slack_bolt import App
from dotenv import load_dotenv
from payloads.app_home_opened import app_home_opened_payload
from payloads.modal_change_request import modal_change_request

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("app_home_opened")
def app_home_opened(client, event, logger):
  try:
    client.views_publish(
      user_id = event["user"],
      view = app_home_opened_payload
    )
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")


@app.action("request_change")
def open_change_request(ack, body, client, logger):
  try:
    ack()
    client.views_open(
      trigger_id = body["trigger_id"],
      view = modal_change_request
    )
  except Exception as e:
    logger.error(f"Error opening change request form: {e}")


@app.view("change_request_view")
def handle_submission(ack, body, client, view):
  user = body['user']
  ack()

  msg = ""
  try:
      msg = f"{user['name']}, your request was successfully sent"
  except Exception as e:
      msg = "There was an error with your submission"
  finally:
      client.chat_postMessage(channel = user['id'], text = msg)

@app.action("selection_environment")
def selection_environment(ack, body, client, logger):
  ack()

@app.action("selection_group")
def selection_group(ack, body, client, logger):
  ack()

@app.action("selection_switcher")
def selection_switcher(ack, body, client, logger):
  ack()

@app.action("selection_switcher")
def selection_switcher(ack, body, client, logger):
  ack()

@app.action("selection_status")
def selection_status(ack, body, client, logger):
  ack()

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
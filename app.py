import os
from slack_bolt import App
from dotenv import load_dotenv
from payloads.app_home_opened import app_home_opened_payload

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

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
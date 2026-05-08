import logging

from events.request_change import RequestChangeEventHandler
from controller.slack_app import SlackAppHandler
from utils.logging_config import configure_logging

LOGGER = logging.getLogger(__name__)

slack_handler = SlackAppHandler()
request_change_handler = RequestChangeEventHandler()

# Build App
configure_logging()
app = slack_handler.build_app()

# Register App Events
request_change_handler.register_events(app)

# Register App APIs
slack_app = slack_handler.register_handler(app)

if __name__ == "__main__":
    LOGGER.info("Starting Slack App...")
    slack_app.run()

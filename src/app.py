from events.request_change import RequestChangeEventHandler
from controller.slack_app import SlackAppHandler

slack_handler = SlackAppHandler()
request_change_handler = RequestChangeEventHandler()

# Build App
app = slack_handler.build_app()

# Register App Events
request_change_handler.register_events(app)

# Register App APIs 
slack_app = slack_handler.register_handler(app)

if __name__ == "__main__":
    slack_app.run()
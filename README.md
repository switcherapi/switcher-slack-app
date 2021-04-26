# Requirements  
- Python 3
- VirtualEnv
- Ngrok

# About  
**Switcher API App** is a Slack App that can be integrated with your Slack workspace in order to control feature change requests.
The API is responsible to handle all requests made through the linked Slack workspace.<br>

# Installing

1. Select the Add app on your workspace and search for Switcher API
2. Follow the instructions to give the app the necessary privileges
3. Confirm the channel ID that will handle the approvals

# Installing: Running locally

### Setup the environment

> 1. **Setup**
Create a *.env* file containing the following:

```
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
```

> 2. **Running the API**
Start the API by running: py app.py

> 3. **Start ngrok**
Expose the API using ngrok, for example: ngrok http 3000

> 4. **Subscribe to events**
Copy the provided ngrok HTTPS URL and add '/slack/events' to it.
Once you have the URL ready to go, open the Slack App, update the Request URL on 'Event Subscription' and also on the 'Interactive & Shortcuts' tab.
Save all changes.

### Switcher Slack App

The following workflow is still in progress and might have changes.

> Change Request Workflow

![Slack App - Change Request](https://raw.githubusercontent.com/petruki/switcher-slack-app/master/docs/change_request_view.jpg)
# About  
**Switcher API App** is a Slack App that can be integrated with your Slack workspace in order to control feature change requests.
The API is responsible to handle all requests made through the linked Slack workspace.<br>

![Slack App - Change Request](https://raw.githubusercontent.com/petruki/switcher-slack-app/master/docs/change_request_view.jpg)

# Installing

### Requirements  
- Python 3
- VirtualEnv
- Ngrok

1. Select the Add app on your workspace and search for Switcher API
2. Follow the instructions to give the app the necessary privileges
3. Confirm the channel ID that will handle the approvals

# Installing: Running locally

### Setup the environment

> 1. **Setup**
Create a *.env* file containing the following:

```
SLACK_SIGNING_SECRET=""
SLACK_CLIENT_ID=""
SLACK_CLIENT_SECRET=""

SWITCHER_URL="https://switcherapi.github.io/switcher-management"
SWITCHER_STORE_URL="http://localhost:3000"
SWITCHER_JWT_SECRET=""
```

> 2. **Running the API**
Start the API by running: py .\src\app.py

> 3. **Start ngrok**
Expose the API using ngrok, for example: ngrok http 5000

> 4. **Subscribe to events**
Copy the provided ngrok HTTPS URL and add '/slack/events' to it.
Once you have the URL ready to go, open the Slack App, update the Request URL on 'Event Subscription' and also on the 'Interactive & Shortcuts' tab.
Save all changes.

### Contributing

You are more than welcome to contribute to the project. 
Here are some important rules:

1. Suggestions: Open a discussion topic and describe clearly what you have in mind.
2. Fix: Open an issue if you found a bug.
3. Solution: Open a PR in case we agreed upon your change suggestion discussed before.

Below some basics steps that you probably are familiar with when contributing to open source projects, but just to make sure.

- (Before) Check if all tests are passing:
```
nosetests
```

- (After) Check if all tests are passing and it covers all possibilities 
```
nosetests --with-coverage --cover-erase --cover-package=src --cover-html
```
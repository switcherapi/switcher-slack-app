[![Build Status](https://travis-ci.com/switcherapi/switcher-slack-app.svg?branch=master)](https://travis-ci.com/switcherapi/switcher-slack-app)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=switcherapi_switcher-slack-app&metric=alert_status)](https://sonarcloud.io/dashboard?id=switcherapi_switcher-slack-app)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=switcherapi_switcher-slack-app&metric=coverage)](https://sonarcloud.io/dashboard?id=switcherapi_switcher-slack-app)
[![Known Vulnerabilities](https://snyk.io/test/github/switcherapi/switcher-slack-app/badge.svg)](https://snyk.io/test/github/switcherapi/switcher-slack-app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Slack: Switcher-HQ](https://img.shields.io/badge/slack-@switcher/hq-blue.svg?logo=slack)](https://switcher-hq.slack.com/)


![Switcher Slack App](https://raw.githubusercontent.com/switcherapi/switcherapi-assets/master/samples/slack/logo.png)

# About
**Switcher Slack App** is a Slack App that can be used to control Switchers from your team or organization workspace.</br>
Features included in this app are described below with examples:

> **Change Request**

Open change requests selecting the Switcher or Group of Switchers to be changed.

![Slack App - Change Request](https://raw.githubusercontent.com/switcherapi/switcherapi-assets/master/samples/slack/change_request_modal.png)

Review your request and add some remarks to justify the change.

![Slack App - Change Request](https://raw.githubusercontent.com/switcherapi/switcherapi-assets/master/samples/slack/change_request_review.png)

A summary message containing all details about the change will be sent to a specific group that was choosen during the installation of the app.

![Slack App - Change Request](https://raw.githubusercontent.com/switcherapi/switcherapi-assets/master/samples/slack/change_request_approval.png)

* * *

# Running locally

### Requirements  
- Python 3
- VirtualEnv
- Ngrok

1. Select the Add app on your workspace and search for Switcher API
2. Follow the instructions to give the app the necessary privileges
3. Confirm the channel ID that will handle the approvals

### Setup the environment

> 1. **Setup**
Create a *.env* file containing the following:

```
SLACK_SIGNING_SECRET=""
SLACK_CLIENT_ID=""
SLACK_CLIENT_SECRET=""

SWITCHER_URL="https://switcherapi.github.io/switcher-management"
SWITCHER_API_URL="http://localhost:3000"
SWITCHER_JWT_SECRET=""
```

> 2. **Running the API**

1. Create a new Virtual Env
2. Install dependencies: pip install -r requirements.txt
3. Start the API by running: py .\src\app.py

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

> (Before) Check if all tests are passing:

```
pytest
```

> (After) Check if all tests are passing and it covers all possibilities 

```
pytest --cov=src

----------- coverage: platform win32, python 3.9.1-final-0 -----------
Name                               Stmts   Miss  Cover
------------------------------------------------------
src\app.py                            73      2    97%
src\controller\__init__.py             0      0   100%
src\controller\change_request.py     102     11    89%
src\controller\home.py                22      4    82%
src\errors\__init__.py                12      0   100%
src\payloads\__init__.py               0      0   100%
src\payloads\change_request.py        27      0   100%
src\payloads\home.py                   2      0   100%
src\services\__init__.py               0      0   100%
src\services\switcher_client.py       32      1    97%
src\services\switcher_service.py      51      1    98%
src\services\switcher_store.py        19      3    84%
src\store\__init__.py                  0      0   100%
src\store\switcher_store.py           73     27    63%
src\utils\__init__.py                  0      0   100%
src\utils\slack_payload_util.py       33      0   100%
src\utils\switcher_util.py            21      0   100%
------------------------------------------------------
TOTAL                                467     49    90%
```


* * *

## Donations
Donations for coffee, cookies or pizza are extremely welcomed.</br>
Please, find the sponsor button at the top for more options.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9FKW64V67RKXW&source=url)
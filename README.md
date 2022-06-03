***

<div align="center">
<b>Switcher Slack App</b><br>
Control & Communicate Switcher changes
</div>

<div align="center">

[![Build Status](https://app.travis-ci.com/switcherapi/switcher-slack-app.svg?branch=master)](https://app.travis-ci.com/switcherapi/switcher-slack-app)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=switcherapi_switcher-slack-app&metric=alert_status)](https://sonarcloud.io/dashboard?id=switcherapi_switcher-slack-app)
[![Known Vulnerabilities](https://snyk.io/test/github/switcherapi/switcher-slack-app/badge.svg)](https://snyk.io/test/github/switcherapi/switcher-slack-app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Slack: Switcher-HQ](https://img.shields.io/badge/slack-@switcher/hq-blue.svg?logo=slack)](https://switcher-hq.slack.com/)

</div>

***


![Switcher Slack App](https://raw.githubusercontent.com/switcherapi/switcherapi-assets/master/samples/slack/logo.png)

# About
**Switcher Slack App** is a Slack App that can be used to control Switchers from your Slack workspace.</br>
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

## Requirements  
- Python 3
- VirtualEnv
- Ngrok

## Create Slack App

The steps below will guide you through the process of creating a Slack App.<br>
Assuming that you have signed up for a Slack account and are logged in to a Workspace.

### Slack: Creating the App

1. Open https://api.slack.com/
2. Click on 'Your Apps'
3. Hit 'Create an App' and then select 'From an app manifest'
4. Select the Workspace to install the app
5. Open 'switcher-slack-app.yaml' and replace the EDNPOINTS with the app URL e.g. https://switcher-slack-app.ngrok.io
6. Copy all the content and paste to the manifest YAML space, then hit next
7. Review the summary provided, then click on 'Create'

(*) Do not install the app via 'Install to Workspace' button

### App: Configure & Deploy
1. Create a new Virtual Env
2. Install dependencies: pip install -r requirements.txt
3. Copy the values Client ID, Secret and Signing Secret.
4. Create a .env file based on .env.template and paste the copied values.
5. Make sure that the SWITCHER_JWT_SECRET matches the Switcher API env value for SWITCHER_SLACK_JWT_SECRET
6. Make sure that Switcher Management has SWITCHERSLACKAPP_URL set to the app URL
7. Start the API by running: py .\src\app.py

## Contributing

You are more than welcome to contribute to the project. 
Here are some important guidelines:

1. Suggestions: Open a discussion topic or issue and describe clearly what you have in mind.
2. Fix: Open an issue if you found a bug.
3. Solution: Open a PR in case we agreed upon your change suggestion discussed before.

Below some basics steps that you probably are familiar with when contributing to open source projects.

> (Before) Check if all tests are passing:

```
pytest
```

> (After) Check if all tests are passing and covers the change being made:

```
pytest --cov=src

----------- coverage: platform win32, python 3.9.1-final-0 -----------
Name                               Stmts   Miss  Cover
------------------------------------------------------
src\app.py                            73      2    97%
src\controller\__init__.py             0      0   100%
src\controller\change_request.py     104     11    89%
src\controller\home.py                22      4    82%
src\errors\__init__.py                13      0   100%
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
TOTAL                                470     49    90%
```


* * *

## Donations
Donations for coffee, cookies or pizza are extremely welcomed.</br>
Please, find the sponsor button at the top for more options.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9FKW64V67RKXW&source=url)
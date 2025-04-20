***

<div align="center">
<b>Switcher Slack App</b><br>
Control & Communicate Switcher changes
</div>

<div align="center">

[![Master CI](https://github.com/switcherapi/switcher-slack-app/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/switcherapi/switcher-slack-app/actions/workflows/master.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=switcherapi_switcher-slack-app&metric=alert_status)](https://sonarcloud.io/dashboard?id=switcherapi_switcher-slack-app)
[![Known Vulnerabilities](https://snyk.io/test/github/switcherapi/switcher-slack-app/badge.svg)](https://snyk.io/test/github/switcherapi/switcher-slack-app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Hub](https://img.shields.io/docker/pulls/trackerforce/switcher-slack-app.svg)](https://hub.docker.com/r/trackerforce/switcher-slack-app)
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
- Python 3.13
- VirtualEnv
- Ngrok (Slack Apps requires HTTPS endpoint)

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

In order to install the app, you will need to run `https://[SWITCHER_SLACK_APP_ENDPOINT]/slack/install` in your browser.<br>
This will trigger the callback to Switcher Management [SWITCHER_URL] to proceed with the Domain authorization.

### App: Configure & Deploy
1. Create a new Virtual Env
2. Install dependencies: `make install`
3. Copy the values Client ID, Secret and Signing Secret.
4. Create a .env file based on .env.template and paste the copied values.
5. Make sure that the SWITCHER_JWT_SECRET matches the Switcher API env value for SWITCHER_SLACK_JWT_SECRET
6. Make sure that Switcher Management has SWITCHERSLACKAPP_URL set to the app URL
7. Start the API by running: `make run`

## Contributing

You are more than welcome to contribute to the project. 
Here are some important guidelines:

1. Suggestions: Open a discussion topic or issue and describe clearly what you have in mind.
2. Fix: Open an issue if you found a bug.
3. Solution: Open a PR in case we agreed upon your change suggestion discussed before.

Below some basics steps that you probably are familiar with when contributing to open source projects.

[Before] Check if all tests are passing:

```
make install-test
make test
```

[Chaging] Check if all tests are passing and covers the change being made:

```
make test
make cover
```
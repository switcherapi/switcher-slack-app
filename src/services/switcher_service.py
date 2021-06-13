import os
import json

from typing import Optional
from .switcher_client import SwitcherClient

class SwitcherService(SwitcherClient):
    """Service responsible for handling all API requests execution against the linked Domain"""

    def __init__(self, *, api_url: Optional[str] = None):
        SwitcherClient.__init__(
            self, 
            api_url or os.environ.get("SWITCHER_API_URL")
        )

    def get_environments(self, team_id: str) -> [str]:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(slack_team_id: "{team_id}") {{
                    environments
                }}
            }}
        ''')

        configuration = response.get("configuration", None)
        if configuration is not None:
            environments = configuration.get("environments", None)
            if environments is not None:
                return environments
        return []

    def get_groups(self, team_id: str, environment: str) -> [dict]:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(
                    slack_team_id: "{team_id}", 
                    environment: "{environment}") 
                {{
                    group {{
                        name
                        activated
                    }}
                }}
            }}
        ''')

        configuration = response.get("configuration", None)
        if configuration is not None:
            groups = configuration.get("group", None)
            if groups is not None:
                return groups

    def get_switchers(self, team_id: str, environment: str, group: str) -> [dict]:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(
                    slack_team_id: "{team_id}", 
                    environment: "{environment}",
                    group: "{group}") 
                {{
                    config {{
                        key
                        activated
                    }}
                }}
            }}
        ''')

        configuration = response.get("configuration", None)
        if configuration is not None:
            configs = configuration.get("config", None)
            if configs is not None:
                return configs

    def validate_ticket(self, team_id: str, context: dict):
        """Validates if Ticket content is valid"""
        
        response = self.do_post(
            path = "/slack/v1/ticket/validate",
            body = {
                "team_id": team_id,
                "ticket_content": {
                    "environment": context["environment"],
                    "group": context["group"],
                    "switcher": context["switcher"],
                    "status": context["status"],
                }
            }
        )

        if response.status_code != 200:
            data = json.loads(response.data.decode('UTF-8'))
            raise Exception(data.get("error", "Try it again later"))

    def create_ticket(self, team_id: str, context: dict) -> dict:
        """Create Ticket and return its ID and Channel to be published"""

        return {
            "ticket_id": "ticket123",
            "channel_id": "C01SH298R6C"
        }

    def approve_request(self, team_id: str, ticket_id: str):
        pass

    def deny_request(self, team_id: str, ticket_id: str):
        pass
import os
import json

from typing import Optional
from errors import SwitcherValidationError
from .switcher_client import SwitcherClient

class SwitcherService(SwitcherClient):
    """ Service responsible for handling all API requests execution against the linked Domain """

    def __init__(self, *, api_url: Optional[str] = None):
        SwitcherClient.__init__(
            self, 
            api_url or os.environ.get("SWITCHER_API_URL") or ""
        )

    def get_domains(self, team_id: str) -> list[dict]:
        response = self.do_get(
            path = "/slack/v1/domains",
            params = {
                "team_id": team_id
            }
        )
        
        if response.status_code != 200:
            raise SwitcherValidationError("Error fetching domains")
        
        return json.loads(response.data.decode('UTF-8'))

    def get_environments(self, team_id: str, domain_id: str) -> list[str] | None:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(
                    slack_team_id: "{team_id}",
                    domain: "{domain_id}")
                {{
                    environments
                }}
            }}
        ''')

        configuration = response.get("configuration", None)
        if configuration is not None:
            environments = configuration.get("environments", None)
            if environments is not None:
                return environments

    def get_groups(self, team_id: str, domain_id: str, environment: str) -> list[dict] | None:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(
                    slack_team_id: "{team_id}", 
                    domain: "{domain_id}",
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

    def get_switchers(self, team_id: str, domain_id: str, environment: str, group: str) -> list[dict] | None:
        response: dict = self.do_graphql(f'''
            query {{
                configuration(
                    slack_team_id: "{team_id}",
                    domain: "{domain_id}",
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

    def validate_ticket(self, team_id: str, context: dict) -> str:
        """ Validates if Ticket content is valid """
        
        response = self.do_post(
            path = "/slack/v1/ticket/validate",
            body = {
                "team_id": team_id,
                "domain_id": context["domain_id"],
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
            raise SwitcherValidationError(data.get("error"))
        
        data = json.loads(response.data.decode('UTF-8'))
        return data.get("result")

    def create_ticket(self, team_id: str, context: dict) -> dict:
        """ Create Ticket and return its ID and Channel to be published """

        response = self.do_post(
            path = "/slack/v1/ticket/create",
            body = {
                "team_id": team_id,
                "domain_id": context["domain_id"],
                "ticket_content": {
                    "environment": context["environment"],
                    "group": context["group"],
                    "switcher": context["switcher"],
                    "status": context["status"],
                    "observations": context["observations"],
                }
            }
        )

        data = json.loads(response.data.decode('UTF-8'))
        if response.status_code != 201:
            raise SwitcherValidationError(data.get("error"))

        return {
            "ticket_id": data.get("ticket")["_id"],
            "channel_id": data.get("channel_id")
        }

    def approve_request(self, team_id: str, domain_id: str, ticket_id: str):
        """ Dispatch change request approval """
        self.__process_request__(team_id, domain_id, ticket_id, True)

    def deny_request(self, team_id: str, domain_id: str, ticket_id: str):
        """ Dispatch change request denied """
        self.__process_request__(team_id, domain_id, ticket_id, False)

    def __process_request__(self, 
        team_id: str, 
        domain_id: str,
        ticket_id: str, 
        approved: bool
    ) -> str:
        """ Dispatch change request approval action """

        response = self.do_post(
            path = "/slack/v1/ticket/process",
            body = {
                "team_id": team_id,
                "domain_id": domain_id,
                "ticket_id": ticket_id,
                "approved": approved
            }
        )

        data = json.loads(response.data.decode('UTF-8'))
        if response.status_code != 200:
            raise SwitcherValidationError(data.get("error"))

        return data.get("message")
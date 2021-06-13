import os
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

import os

from flask import Response
from typing import Optional
from .switcher_service import SwitcherService

class SwitcherInstallationStoreService(SwitcherService):
    """Service responsible to handle the app installation and authentication"""

    def __init__(self, *, api_url: Optional[str] = None):
        SwitcherService.__init__(
            self, 
            api_url or os.environ.get("SWITCHER_STORE_URL")
        )

    def save_installation(
        self,
        enterprise_id: str,
        team_id: str, 
        user_id: str, 
        installation_payload: dict,
        bot_payload: dict
    ) -> Response:
        return self.do_post(
            path = "/slack/v1/installation",
            body = {
                "enterprise_id": enterprise_id,
                "team_id": team_id,
                "user_id": user_id,
                "installation_payload": installation_payload,
                "bot_payload": bot_payload
            }
        )

    def find_bot(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str]
    ) -> Response:
        return self.do_get(
            path = "/slack/v1/findbot",
            params = {
                "enterprise_id": enterprise_id,
                "team_id": team_id
            }
        )

    def find_installation(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str]
    ) -> Response:
        return self.do_get(
            path = "/slack/v1/findinstallation",
            params = {
                "enterprise_id": enterprise_id,
                "team_id": team_id
            }
        )
        
    def delete_installation(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str],
        user_id: Optional[str] = None
    ) -> Response:
        return self.do_delete(
            path = "/slack/v1/deleteinstallation",
            params = {
                "enterprise_id": enterprise_id,
                "team_id": team_id,
                "user_id": user_id
            }
        )

    def delete_bot(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str],
        user_id: Optional[str] = None
    ) -> Response:
        return self.do_delete(
            path = "/slack/v1/deletebot",
            params = {
                "enterprise_id": enterprise_id,
                "team_id": team_id,
                "user_id": user_id
            }
        )
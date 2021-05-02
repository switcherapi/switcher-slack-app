import os
import requests

from flask import Response
from typing import Optional

class SwitcherInstallationStoreService:
    api_url: str

    def __init__(
        self,
        *,
        api_url: Optional[str] = None
    ):
        self.api_url = api_url or os.environ.get("SWITCHER_STORE_URL")

    def save_installation(
        self,
        enterprise_id: str,
        team_id: str, 
        user_id: str, 
        installation_payload: dict,
        bot_payload: dict
    ) -> Response:
        return self._responseHandler(requests.post(
                url = f"{self.api_url}/slack/v1/installation",
                json = {
                    "enterprise_id": enterprise_id,
                    "team_id": team_id,
                    "user_id": user_id,
                    "installation_payload": installation_payload,
                    "bot_payload": bot_payload
                }
            )
        )

    def find_bot(
        self, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> Response:
        return self._responseHandler(requests.get(
                url = f"{self.api_url}/slack/v1/findbot",
                params = {
                    "enterprise_id": enterprise_id,
                    "team_id": team_id
                }
            )
        )

    def find_installation(
        self, enterprise_id: Optional[str], team_id: Optional[str]
    ) -> Response:
        return self._responseHandler(requests.get(
                url = f"{self.api_url}/slack/v1/findinstallation",
                params = {
                    "enterprise_id": enterprise_id,
                    "team_id": team_id
                }
            )
        )
        
    def delete_installation(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str],
        user_id: Optional[str] = None
    ) -> Response:
        return self._responseHandler(requests.delete(
                url = f"{self.api_url}/slack/v1/deleteinstallation",
                params = {
                    "enterprise_id": enterprise_id,
                    "team_id": team_id,
                    "user_id": user_id
                }
            )
        )

    def delete_bot(
        self, 
        enterprise_id: Optional[str], 
        team_id: Optional[str],
        user_id: Optional[str] = None
    ) -> Response:
        return self._responseHandler(requests.delete(
                url = f"{self.api_url}/slack/v1/deletebot",
                params = {
                    "enterprise_id": enterprise_id,
                    "team_id": team_id,
                    "user_id": user_id
                }
            )
        )
        
    @staticmethod
    def _responseHandler(response: Response) -> Response:
        return Response(
            response = response.content,
            status = response.status_code,
            mimetype = "application/json"
        )
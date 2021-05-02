import os
import requests

from flask import Response
from typing import Optional

class SwitcherService:
    api_url: str

    def __init__(
        self,
        *,
        api_url: Optional[str] = None
    ):
        self.api_url = api_url or os.environ.get("SWITCHER_API_URL")

    def saveInstallation(
        self,
        team_id: str, 
        user_id: str, 
        installation_payload: dict,
        bot_payload: dict
    ) -> None:
        response = requests.post(
            url = f"{self.api_url}/slack/v1/installation",
            json = {
                "team_id": team_id,
                "user_id": user_id,
                "installation_payload": installation_payload,
                "bot_payload": bot_payload
            }
        )

        return Response(
            response = response.content,
            status = response.status_code,
            mimetype = "application/json"
        )
import os
import datetime
import jwt
import requests

from flask import Response
from typing import Optional

class SwitcherService:
    """Default Switcher Service implementation"""

    def __init__(self, api_url: str):
        self.__secret = os.environ.get("SWITCHER_JWT_SECRET")
        self.__algorithm: str = "HS256"
        self.__issuer: str = "Switcher Slack App"
        self._api_url = api_url

    def do_post(self, path: str, body: Optional[dict]) -> Response:
        return self.__response_handler(requests.post(
                **self.__request_builder(
                    url = self._api_url + path,
                    resource = path
                ),
                json = body
            )
        )

    def do_get(self, path: str, params: Optional[dict]) -> Response:
        return self.__response_handler(requests.get(
                **self.__request_builder(
                    url = self._api_url + path,
                    resource = path
                ),
                params = params
            )
        )

    def do_delete(self, path: str, params: Optional[dict]) -> Response:
        return self.__response_handler(requests.delete(
                **self.__request_builder(
                    url = self._api_url + path,
                    resource = path
                ),
                params = params
            )
        )

    def __generate_token(self, resource: str) -> str:
        return jwt.encode(
            key = self.__secret,
            algorithm = self.__algorithm,
            payload = {
                "iss": self.__issuer,
                "sub": resource,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = 30)
            }
        )

    def __request_builder(self, url: str, resource: str) -> dict:
        return {
            "url": url,
            "headers": { 
                "Authorization": f"Bearer {self.__generate_token(resource)}"
            }
        }

    def __response_handler(self, response: Response) -> Response:
        return Response(
            response = response.content,
            status = response.status_code,
            mimetype = "application/json"
        )
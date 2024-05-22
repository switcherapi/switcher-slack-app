import os
import datetime
import jwt
import requests

from flask import Response
from typing import Optional

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class SwitcherClient:
    """ Switcher Client wraps HTTP request against the Swicther API """

    def __init__(self, api_url: str):
        self.__secret = os.environ.get("SWITCHER_JWT_SECRET")
        self.__algorithm: str = "HS256"
        self.__issuer: str = "Switcher Slack App"
        self._api_url = api_url

    def do_post(self, path: str, body: Optional[dict]) -> Response:
        return self.__response_handler__(requests.post(
                **self.__request_builder__(
                    url = self._api_url + path,
                    resource = path
                ),
                json = body
            )
        )

    def do_get(self, path: str, params: Optional[dict]) -> Response:
        return self.__response_handler__(requests.get(
                **self.__request_builder__(
                    url = self._api_url + path,
                    resource = path
                ),
                params = params
            )
        )

    def do_delete(self, path: str, params: Optional[dict]) -> Response:
        return self.__response_handler__(requests.delete(
                **self.__request_builder__(
                    url = self._api_url + path,
                    resource = path
                ),
                params = params
            )
        )

    def do_graphql(self, query: str) -> dict:
        client = self.__gql_client__("slack-graphql")
        query = gql(query)
        return client.execute(query)

    def __generate_token__(self, resource: str) -> str:
        return jwt.encode(
            key = self.__secret,
            algorithm = self.__algorithm,
            payload = {
                "iss": self.__issuer,
                "sub": resource,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds = 30)
            }
        )

    def __request_builder__(self, url: str, resource: str) -> dict:
        return {
            "url": url,
            "headers": { 
                "Authorization": f"Bearer {self.__generate_token__(resource)}"
            }
        }

    def __response_handler__(self, response) -> Response:
        return Response(
            response = response.content,
            status = response.status_code,
            mimetype = "application/json"
        )

    def __gql_client__(self, resource: str) -> Client:
        return Client(
            fetch_schema_from_transport = True,
            transport = RequestsHTTPTransport(
                url = f'{self._api_url}/slack-graphql',
                headers = {
                    "Content-type": "application/json",
                    "Authorization": f"Bearer {self.__generate_token__(resource)}"
                },
                use_json = True,
                verify = False,
                retries = 3
            )
        )
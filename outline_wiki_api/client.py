import json
import requests
from outline_wiki_api import utils
from outline_wiki_api.models import (
    auth,
    users,
    documents,
    collections
)
from typing import Optional


class OutlineWiki:

    def __init__(
            self,
            url: Optional[str] = None,
            token: Optional[str] = None,
            ssl_verify: Optional[bool] = None
    ) -> None:
        self._base_url = utils.get_base_url(url)
        self._url = f'{self._base_url}/api'
        self._token = token
        self.ssl_verify = ssl_verify
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.auth = auth.Auth(client=self)
        self.users = users.Users(client=self)
        self.collections = collections.Collections(client=self)
        self.documents = documents.Documents(client=self)

    @property
    def url(self):
        return self._base_url

    @property
    def api_url(self):
        return self._url

    @property
    def token(self):
        return self._token

    def post(self,
             method: str,
             data: Optional[dict] = None,
             params: Optional[dict] = None,
             **kwargs) -> requests.Response:
        request_url = f'{self._url}/{method}'
        print(request_url)
        result = requests.post(
            url=request_url,
            json=data,
            params=params,
            headers=self.headers,
            **kwargs
        )
        return result


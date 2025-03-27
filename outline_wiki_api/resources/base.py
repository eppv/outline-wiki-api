
import json
from typing import Optional, Dict
from ..client import Client


class Resources:

    _path: str

    def __init__(self, client: Client):
        self._client = client

    def post(self,
             endpoint: str,
             params: Optional[Dict] = None,
             data: Optional[Dict] = None):
        response = self._client.request(
            method="POST",
            endpoint=endpoint,
            params=params,
            data=data
        )
        return response

    def info(self, data: Optional[Dict] = None):
        """
        Retrieve an entity
        :return:
        """
        endpoint = f'/{self._path}.info'
        return self.post(
            endpoint=endpoint,
            data=data
        )




import json
from typing import Optional
from ..client import Client


class Resources:

    _path: str

    def __init__(self, client: Client):
        self._client = client

    def info(self,
             data: Optional[dict] = None
             ):
        """
        Retrieve an entity
        :return:
        """
        method = f'{self._path}.info'
        return self._client.request(
            method=method,
            data=data
        )



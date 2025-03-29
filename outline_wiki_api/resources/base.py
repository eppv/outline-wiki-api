
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
             data: Optional[Dict] = None,
             files: Optional[Dict] = None,
             **kwargs):
        full_endpoint = f"{self._path}.{endpoint}"
        response = self._client.request(
            method="POST",
            endpoint=full_endpoint,
            params=params,
            data=data,
            files=files,
            **kwargs
        )
        return response




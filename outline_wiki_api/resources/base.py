
import json
from httpx import Response
from typing import Optional, Dict, Any
from ..client import Client


class Resources:
    """
    The base parent class for API resources.
    It has no practical use by itself.
    """
    _path: str

    def __init__(self, client: Client):
        self._client = client

    def post(self,
             endpoint: str,
             params: Optional[Dict] = None,
             data: Optional[Dict] = None,
             files: Optional[Dict] = None,
             **kwargs) -> Response:
        """
        POST HTTP-request for the exact resource.
        All Outline API endpoints currently accept only POST requests.

        Args:
            endpoint: The last part of the endpoint URL, the name of the method being called.
            params: POST-request parameters (It is practically not used in this API.)
            data: Data payload for request with `application/json` content type (most endpoints).
            files: Data payload for requests with `multipart/form-data` content type.

        Returns:
            httpx Response object
        """
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




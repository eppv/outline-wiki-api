import httpx
import logging
from typing import Optional, Dict, Any
from .exceptions import OutlineAPIError, OutlineAuthenticationError

log = logging.getLogger(__name__)


class Client:

    def __init__(
            self,
            url: Optional[str] = None,
            token: Optional[str] = None,
            timeout: float = 30.0,
            ssl_verify: Optional[bool] = None
    ) -> None:
        self._base_url = url
        self._url = f'{self._base_url}/api'
        self._token = token
        self._timeout = timeout
        self._ssl_verify = ssl_verify
        self._headers = {
            'Authorization': f'Bearer {self._token}'
        }
        self._client = httpx.Client(
            base_url=self._url,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._ssl_verify
        )

    @property
    def url(self):
        return self._base_url

    @property
    def api_url(self):
        return self._url

    def request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            data: Optional[Dict] = None,
            files: Optional[Dict] = None,
            **kwargs
    ) -> Any:
        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=data,
                files=files,
                **kwargs
            )
            log.debug(f"Request headers: {response.request.headers}")
            log.debug(f"Request content: {response.request.read()}")
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise OutlineAuthenticationError("Invalid API key") from e
            raise OutlineAPIError(
                f'API request failed: {e.response.text}', status_code=e.response.status_code
            ) from e
        except httpx.RequestError as e:
            raise OutlineAPIError(f'Request failed: {str(e)}') from e

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


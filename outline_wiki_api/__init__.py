from typing import Optional
from .client import Client
from .utils import get_base_url
from .resources.documents import Documents
from .resources.collections import Collections
from .resources.auth import Auth
from .models import Document, Collection, User


class Outline:
    def __init__(
            self,
            token: str,
            url: Optional[str] = None
    ) -> None:
        self.url = get_base_url(url)
        self._client = Client(token=token, url=url)
        self.auth = Auth(self._client)
        self.documents = Documents(self._client)
        self.collections = Collections(self._client)
        # Add other resources here

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

import logging
from .client import Client
from .utils import get_base_url, get_token
from .resources.documents import Documents
from .resources.collections import Collections
from .resources.auth import Auth
from .resources.users import Users
from .resources.views import Views
from .resources.events import Events
from .resources.comments import Comments


class OutlineWiki:
    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        logging_level: int = logging.WARNING,
    ) -> None:
        self.url = get_base_url(url)
        self._token = get_token(token)
        self._client = Client(token=self._token, url=self.url)
        self.auth = Auth(self._client)
        self.documents = Documents(self._client)
        self.collections = Collections(self._client)
        self.users = Users(self._client)
        self.views = Views(self._client)
        self.events = Events(self._client)
        self.comments = Comments(self._client)
        # TODO: Add other resources here
        logging.basicConfig(
            level=logging_level,
            format="%(asctime)s - %(name)s: %(levelname)s: %(message)s",
        )

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

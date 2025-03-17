
import json
from typing import Optional


class EntityCollection:

    _path: str

    def __init__(
            self,
            client
    ):
        self.client = client

    def info(self,
             data: Optional[dict] = None
             ):
        """
        Retrieve an entity
        :return:
        """
        method = f'{self._path}.info'
        return self.client.post(
            method=method,
            data=data
        )



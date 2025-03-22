
from typing import Optional
from outline_wiki_api.base import EntityCollection


class Auth(EntityCollection):
    _path = 'auth'

    def __init__(self, client):
        super().__init__(client)
        self._user_id: Optional[str] = None

    def init(self):
        data = self.info().json()['data']
        setattr(self, 'user_id', data['user']['id'])

    @property
    def user_id(self):
        return self._user_id

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        method = f'{self._path}.config'
        return self.client.post(method=method)

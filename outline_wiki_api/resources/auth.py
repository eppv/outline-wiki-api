
from .base import Resources
from ..models import User


class Auth(Resources):
    _path = 'auth'

    def __init__(self, client):
        super().__init__(client)
        self._user_id = None

    def get_current_user(self):
        response = self.info().json()
        return User(**response['data']['user'])

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        endpoint = f'{self._path}.config'
        return self.post(endpoint=endpoint)

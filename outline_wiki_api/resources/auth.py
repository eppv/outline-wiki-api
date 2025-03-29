
from typing import Optional, Dict
from .base import Resources
from ..models.user import User
from ..models.team import Team


class Auth(Resources):
    """
    `Auth` represents the current API Keys authentication details. It can be
    used to check that a token is still valid and load the IDs for the current
    user and team.
    """
    _path = 'auth'

    def __init__(self, client):
        super().__init__(client)
        self._user_id = None

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

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        endpoint = f'{self._path}.config'
        return self.post(endpoint=endpoint)

    def get_current_user(self):
        response = self.info().json()
        return User(**response['data']['user'])

    def get_current_team(self):
        response = self.info().json()
        return Team(**response['data']['team'])
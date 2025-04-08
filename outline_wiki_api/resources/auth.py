from .base import Resources
from ..models.auth import AuthResponse
from ..models.user import User
from ..models.team import Team


class Auth(Resources):
    """
    `Auth` represents the current API Keys authentication details. It can be
    used to check that a token is still valid and load the IDs for the current
    user and team.
    """
    _path = "/auth"

    def __init__(self, client):
        super().__init__(client)
        self._user_id = None

    def info(self) -> AuthResponse:
        """
        Retrieve authentication info
        :return:
        """
        response = self.post(endpoint="info").json()
        return AuthResponse(**response)

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        endpoint = "config"
        return self.post(endpoint=endpoint)

    def get_current_user(self) -> User:
        """
        Retrieve current User
        """
        auth_info = self.info()
        return auth_info.data.user

    def get_current_team(self) -> Team:
        """
        Retrieve current Team
        """
        auth_info = self.info()
        return auth_info.data.team

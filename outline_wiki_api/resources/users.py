from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from .base import Resources
from ..models.user import UserResponse


class Users(Resources):
    """
    `Users` represent an individual with access to the knowledge base. Users
    can be created automatically when signing in with SSO or when a user is
    invited via email.
    """
    _path: str = '/users'

    def info(self, user_id: Union[str, UUID]) -> UserResponse:
        """
        Retrieves a User object representing an individual with access to the knowledge base.
        Users can be created automatically when signing in with SSO or when a user is invited via email.
        Args:
            user_id:

        Returns:
            UserResponse: a response objects which contains a User object as data
        """

        data = {"id": str(user_id)}
        response = self.post("info", data=data)
        return UserResponse(**response.json())


"""
Classes for Users resources group

Classes:
    Users: Users resources method group main class
"""

from typing import Optional, Union, Literal, List
from pydantic import EmailStr
from uuid import UUID
from .base import Resources
from ..models.user import User, UserRole, UserResponse, UserListResponse
from ..models.response import Pagination, Sort


class Users(Resources):
    """
    `Users` represent an individual with access to the knowledge base. Users
    can be created automatically when signing in with SSO or when a user is
    invited via email.

    Methods:
        info: Retrieves a User object
        list: Retrieves an Array of User objects
        update_role: Change a users role
    """
    _path: str = '/users'

    def info(self, user_id: Union[str, UUID]) -> UserResponse:
        """Retrieves a User object representing an individual with access to the knowledge base.
        Users can be created automatically when signing in with SSO or when a user is invited via email.
        Args:
            user_id: The User to retrieve

        Returns:
            UserResponse: a response objects which contains a User object as data
        """

        data = {"id": str(user_id)}
        response = self.post("info", data=data)
        return UserResponse(**response.json())

    def list(
            self,
            query: Optional[str] = None,
            emails: Optional[List[EmailStr]] = None,
            status: Optional[Literal["all", "invited", "active", "suspended"]] = None,
            role: Optional[UserRole] = None,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sort] = None
    ) -> UserListResponse:
        """
        List and filter all the users in the team

        Args:
            query: A text search query to filter by (searches in username and email)
            emails: An array of emails to filter the output
            status: The status to filter by
            role: The user role to filter by
            pagination: Custom pagination (default: offset=0, limit=25)
            sorting: Custom sorting order (takes `Sort` object)

        Returns:
            UserListResponse: a response objects which contains an array of User objects as data
        """
        data = {"status": status}
        if query:
            data["query"] = query
        if emails:
            data["emails"] = emails
        if status:
            data["status"] = status
        if role:
            data["role"] = role
        if pagination:
            data.update(pagination.dict())
        if sorting:
            data.update(sorting.dict())

        response = self.post("list", data=data)
        return UserListResponse(**response.json())

    def update_role(
            self,
            user_id: Union[str, UUID],
            role: UserRole
    ) -> UserResponse:
        """
        Change the role of a user, only available to admin authorization.

        Args:
            user_id: Unique identifier for the user.
            role: Workspace-wide role

        Returns:
            UserResponse: a response objects which contains a User object as data

        """
        data = {"id": user_id, "role": role}
        response = self.post("update_role", data=data)
        return UserResponse(**response.json())

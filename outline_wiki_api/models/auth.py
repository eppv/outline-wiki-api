"""
Data structures for Authentication resource information and responses
"""

from pydantic import BaseModel, Field

from .response import Response
from .team import Team
from .user import User


class AuthProvider(BaseModel):
    id: str
    name: str
    auth_url: str = Field(..., alias="authUrl")


class AuthInfoData(BaseModel):
    """
    Authentication data for the current API key
    """

    user: User
    team: Team
    groups: list | None = None
    group_users: list | None = Field(None, alias="groupUsers")
    collaboration_token: str = Field(..., alias="collaborationToken")
    available_teams: list | None = Field(None, alias="availableTeams")
    token: str | None = Field(
        None,
        description="Authentication token returned by login and register endpoints",
    )


class AuthConfigData(BaseModel):
    """
    Authentication options
    """

    name: str
    hostname: str | None = None
    services: list[dict] | None = Field([])
    custom_theme: dict | None = Field({}, alias="customTheme")
    providers: list[AuthProvider] | None = None


class AuthResponse(Response):
    """
    Authentication details response for the current API key
    """

    data: AuthInfoData | AuthConfigData | None = None

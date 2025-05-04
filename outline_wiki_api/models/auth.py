"""
Data structures for Authentication resource information and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Union, Dict

from .response import Response
from .user import User
from .team import Team


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
    groups: Optional[List]
    group_users: Optional[List] = Field(..., alias="groupUsers")
    collaboration_token: str = Field(..., alias="collaborationToken")
    available_teams: Optional[List] = Field(..., alias="availableTeams")
    token: Optional[str] = Field(None, description="Authentication token returned by login and register endpoints")


class AuthConfigData(BaseModel):
    """
    Authentication options
    """
    name: str
    hostname: Optional[str] = None
    services: Optional[List[Dict]] = Field([])
    custom_theme: Optional[Dict] = Field({}, alias='customTheme')
    providers: Optional[List[AuthProvider]]


class AuthResponse(Response):
    """
    Authentication details response for the current API key
    """
    data: Optional[Union[AuthInfoData, AuthConfigData]]


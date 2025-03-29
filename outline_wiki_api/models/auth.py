from pydantic import BaseModel, Field
from typing import Optional, List

from .response import Policy
from .user import User
from .team import Team


class AuthData(BaseModel):
    """
    Authentication data for the current API key
    """
    user: User
    team: Team
    groups: Optional[List]
    group_users: Optional[List] = Field(..., alias="groupUsers")
    collaboration_token: str = Field(..., alias="collaborationToken")
    available_teams: Optional[List] = Field(..., alias="availableTeams")


class AuthInfo(BaseModel):
    """
    Authentication details for the current API key
    """
    data: AuthData
    policies: Optional[List[Policy]]
    status: int
    ok: bool


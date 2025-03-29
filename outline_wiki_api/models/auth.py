from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List
from .user import User
from .team import Team


class AuthData(BaseModel):
    user: User
    team: Team
    groups: Optional[List]
    group_users: Optional[List] = Field(..., alias="groupUsers")
    collaboration_token: str = Field(..., alias="collaborationToken")
    available_teams: Optional[List] = Field(..., alias="availableTeams")


class AuthInfo(BaseModel):
    data: AuthData
    policies: Optional[List[Dict]]
    status: int
    ok: bool


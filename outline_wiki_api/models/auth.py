from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List
from .user import User
from .team import Team


class AuthPolicy(BaseModel):
    """
    Most API resources have associated "policies", these objects describe the
    current API keys authorized actions related to an individual resource. It
    should be noted that the policy "id" is identical to the resource it is
    related to, policies themselves do not have unique identifiers.

    For most usecases of the API, policies can be safely ignored. Calling
    unauthorized methods will result in the appropriate response code – these can
    be used in an interface to adjust which elements are visible.
    """
    id: UUID
    abilities: Dict


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
    policies: Optional[List[AuthPolicy]]
    status: int
    ok: bool


from typing import Optional, Dict, List
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from .user import UserRole  # Assuming UserRole is defined in user.py


class Team(BaseModel):
    """
    Represents a team in the system, which is a group of users with shared resources.

    Teams are the primary way to organize users and control access to collections
    and documents. Each team has its own knowledge base with configurable settings.
    """

    id: UUID = Field(
        ...,
        description="Unique identifier for the object",
        read_only=True,
        example="9cb7cb53-0a8f-497d-a8e8-2aff9ee6f2c2"
    )

    name: str = Field(
        ...,
        description="The name of this team, it is usually auto-generated when the "
                    "first SSO connection is made but can be changed if necessary",
        example="Engineering Team"
    )

    avatar_url: Optional[str] = Field(
        None,
        alias='avatarUrl',
        description="The URL for the image associated with this team, it will be "
                    "displayed in the team switcher and in the top left of the "
                    "knowledge base along with the name",
        example="https://example.com/team-avatar.jpg"
    )

    sharing: bool = Field(
        ...,
        description="Whether this team has share links globally enabled. If this "
                    "value is false then all sharing UI and APIs are disabled",
        example=True
    )

    member_collection_create: bool = Field(
        ...,
        alias='memberCollectionCreate',
        description="Whether members are allowed to create new collections. If false "
                    "then only admins can create collections",
        example=True
    )

    member_team_create: bool = Field(
        ...,
        alias='memberTeamCreate',
        description="Whether members are allowed to create new teams",
        example=False
    )

    default_collection_id: Optional[UUID] = Field(
        None,
        alias='defaultCollectionId',
        description="If set then the referenced collection is where users will be "
                    "redirected to after signing in instead of the Home screen",
        example="a1b2c3d4-5678-90ef-1234-567890abcdef"
    )

    default_user_role: Optional[UserRole] = Field(
        None,
        alias='defaultUserRole',
        description="The default role assigned to new users joining this team"
    )

    document_embeds: bool = Field(
        ...,
        alias='documentEmbeds',
        description="Whether this team has embeds in documents globally enabled. "
                    "It can be disabled to reduce potential data leakage to third parties",
        example=True
    )

    guest_sign_in: bool = Field(
        ...,
        alias='guestSignin',
        description="Whether this team has guest signin enabled. Guests can signin "
                    "with an email address and are not required to have a Google "
                    "Workspace/Slack SSO account once invited",
        example=False
    )

    subdomain: Optional[str] = Field(
        None,
        description="Represents the subdomain at which this team's knowledge base "
                    "can be accessed",
        example="engineering",
        pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$"
    )

    domain: Optional[str] = Field(
        None,
        description="Custom domain name for this team's knowledge base",
        example="docs.example.com"
    )

    url: HttpUrl = Field(
        ...,
        description="The fully qualified URL at which this team's knowledge base "
                    "can be accessed",
        read_only=True,
        example="https://app.getoutline.com"
    )

    invite_required: bool = Field(
        ...,
        alias='inviteRequired',
        description="Whether an invite is required to join this team, if false users "
                    "may join with a linked SSO provider",
        example=True
    )

    allowed_domains: Optional[List[str]] = Field(
        None,
        alias='allowedDomains',
        description="List of hostnames that user emails are restricted to",
        example=["example.com", "company.org"]
    )

    preferences: Optional[Dict] = Field(
        None,
        description="Team-specific preferences and settings"
    )

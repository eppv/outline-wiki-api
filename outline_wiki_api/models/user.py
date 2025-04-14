from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from .response import Response


class UserRole(str, Enum):
    """Available user roles in the system"""
    ADMIN = 'admin'
    MEMBER = 'member'
    VIEWER = 'viewer'
    GUEST = 'guest'


class User(BaseModel):
    """
    Represents a user in the system.

    This model contains all the essential information about a user account,
    including personal details, preferences, and activity timestamps.
    """
    id: UUID = Field(
        ...,
        description="Unique identifier for the user in UUID v4 format",
        example="9cb7cb53-0a8f-497d-a8e8-2aff9ee6f2c2"
    )
    name: str = Field(
        ...,
        description="The name of this user, it is migrated from Slack or Google Workspace "
                    "when the SSO connection is made but can be changed if necessary.",
        min_length=1,
        max_length=100,
        example="John Doe"
    )
    avatar_url: Optional[str] = Field(
        None,
        alias='avatarUrl',
        description="The URL for the image associated with this user, "
                    "it will be displayed in the application UI and email notifications.",
        example="https://example.com/avatars/john.jpg"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="The email associated with this user, it is migrated from Slack or Google Workspace "
                    "when the SSO connection is made but can be changed if necessary.",
        example="user@example.com"
    )
    color: Optional[str] = Field(
        None,
        description="User's preferred color in hex format",
        pattern="^#[0-9a-fA-F]{6}$",
        example="#FF5733"
    )
    role: Optional[UserRole] = Field(
        None,
        description="User's role determining access permissions"
    )
    is_suspended: bool = Field(
        ...,
        alias='isSuspended',
        description="Whether the user account is currently suspended",
        example=False
    )
    created_at: datetime = Field(
        ...,
        alias='createdAt',
        description="The date and time that this user first signed in or was invited as a guest.",
        example="2023-01-15T09:30:00Z"
    )
    updated_at: datetime = Field(
        ...,
        alias='updatedAt',
        description="Timestamp when the user account was last updated",
        example="2023-06-20T14:25:00Z"
    )
    last_active_at: Optional[datetime] = Field(
        None,
        alias='lastActiveAt',
        description="The last time this user made an API request, this value is updated at most every 5 minutes.",
        example="2023-07-01T08:15:00Z"
    )
    timezone: Optional[str] = Field(
        None,
        description="User's preferred timezone in IANA format",
        example="America/New_York"
    )
    language: Optional[str] = Field(
        None,
        description="User's preferred language code (ISO 639-1)",
        example="en"
    )
    preferences: Optional[Dict] = Field(
        None,
        description="Dictionary of user-specific preferences and settings"
    )
    notification_settings: Optional[Dict] = Field(
        None,
        alias='notificationSettings',
        description="User's notification preferences and settings"
    )


class UserResponse(Response):
    data: Optional[User] = None


class UserListResponse(Response):
    data: Optional[List[User]] = []


from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str
    name: str
    avatar_url: Optional[str] = Field(..., alias='avatarUrl')
    email: Optional[EmailStr]
    color: Optional[str]
    role: Optional[str]
    is_suspended: bool = Field(..., alias='isSuspended')
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    last_active_at: Optional[datetime] = Field(..., alias='lastActiveAt')
    timezone: Optional[str]
    language: Optional[str]
    preferences: Optional[Dict]
    notification_settings: Optional[Dict] = Field(..., alias='notificationSettings')


class Team(BaseModel):
    id: str
    name: str
    avatar_url: Optional[str] = Field(..., alias='avatarUrl')
    sharing: bool
    member_collection_create: bool = Field(..., alias='memberCollectionCreate')
    member_team_create: bool = Field(..., alias='memberTeamCreate')
    default_collection_id: Optional[str] = Field(..., alias='defaultCollectionId')
    document_embeds: bool = Field(..., alias='documentEmbeds')
    guest_sign_in: bool = Field(..., alias='guestSignin')
    subdomain: Optional[str]
    domain: Optional[str]
    url: str
    defaultUserRole: str = Field(..., alias='defaultUserRole')
    invite_required: bool = Field(..., alias='inviteRequired')
    allowed_domains: Optional[List] = Field(..., alias='allowedDomains')
    preferences: Optional[Dict]


class Collection(BaseModel):
    id: str
    name: str
    description: Optional[str]
    private: bool
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    deleted_at: Optional[datetime] = Field(..., alias='deletedAt')
    documents: Optional[List[Dict[str, Any]]]


class Document(BaseModel):
    id: str
    collection_id: Optional[str] = Field(..., alias='collectionId')
    title: str
    text: str
    url: str
    emoji: Optional[str]
    pinned: bool
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    published_at: Optional[datetime] = Field(..., alias='publishedAt')
    last_modified_by: Optional[User]
    created_by: User
    updated_by: User

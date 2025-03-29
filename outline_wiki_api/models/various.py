from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from .user import User


class Collection(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    private: bool
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    deleted_at: Optional[datetime] = Field(..., alias='deletedAt')
    documents: Optional[List[Dict[str, Any]]]


class Document(BaseModel):
    id: UUID
    collection_id: Optional[str] = Field(..., alias='collectionId')
    title: str
    text: str
    url: str
    emoji: Optional[str]
    pinned: bool
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    published_at: Optional[datetime] = Field(..., alias='publishedAt')
    last_modified_by: Optional[User] = Field(..., alias='lastModifiedBy')
    created_by: User
    updated_by: User



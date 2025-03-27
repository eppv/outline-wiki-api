
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    avatar_url: Optional[str]
    email: Optional[str]
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class Collection(BaseModel):
    id: str
    name: str
    description: Optional[str]
    private: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    documents: Optional[List[Dict[str, Any]]]


class Document(BaseModel):
    id: str
    collection_id: Optional[str]
    title: str
    text: str
    url: str
    emoji: Optional[str]
    pinned: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    last_modified_by: Optional[User]
    created_by: User
    updated_by: User
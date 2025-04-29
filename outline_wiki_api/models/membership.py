from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from .response import Permission


class Membership(BaseModel):
    """
    Represents a membership relationship between a user and a document.
    
    This class defines the structure for document memberships, including
    the user's permission level and associated metadata.
    """
    id: str = Field(..., description="Unique identifier for the membership")
    user_id: UUID = Field(..., alias="userId", description="ID of the user who is a member")
    document_id: Optional[UUID] = Field(None, alias="documentId")
    collection_id: Optional[UUID] = Field(
        None,
        alias="collectionId",
        description="ID of the collection the user is a member of")
    permission: Optional[Permission] = Field(
        ..., 
        description="Permission level for the user on this document"
    )
    created_by_id: Optional[UUID] = Field(..., alias='createdById')
    created_at: Optional[datetime] = Field(
        None,
        alias="createdAt",
        description="When the membership was created")
    updated_at: Optional[datetime] = Field(
        None,
        alias="updatedAt",
        description="When the membership was last updated")
    source_id: Optional[UUID] = Field(
        ...,
        alias="sourceId"
    )
    index: Optional[str]

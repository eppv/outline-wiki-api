from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID


class Membership(BaseModel):
    """
    Represents a membership relationship between a user and a document.
    
    This class defines the structure for document memberships, including
    the user's permission level and associated metadata.
    """
    id: str = Field(..., description="Unique identifier for the membership")
    userId: UUID = Field(..., description="ID of the user who is a member")
    collectionId: UUID = Field(..., description="ID of the collection the user is a member of")
    permission: Literal["read", "read_write"] = Field(
        ..., 
        description="Permission level for the user on this document"
    )
    createdAt: datetime = Field(..., description="When the membership was created")
    updatedAt: datetime = Field(..., description="When the membership was last updated")

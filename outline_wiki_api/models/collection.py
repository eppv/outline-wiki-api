from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from .user import User
from .response import Sort, Response


class Permission(str, Enum):
    """Available permission options for collections"""
    READ = 'read'
    READ_WRITE = 'read_write'


class Collection(BaseModel):
    """
    Represents a collection of documents in the system.

    Collections are used to organize documents into groups with shared permissions
    and settings. They appear in the sidebar navigation.
    """

    id: UUID = Field(
        ...,
        description="Unique identifier for the object",
        read_only=True,
        example="550e8400-e29b-41d4-a716-446655440000"
    )

    url_id: str = Field(
        ...,
        alias='urlId',
        description="A short unique identifier that can be used to identify the "
                    "collection instead of the UUID",
        read_only=True,
        example="hDYep1TPAM",
        min_length=8,
        max_length=16
    )

    name: str = Field(
        ...,
        description="The name of the collection",
        example="Human Resources",
        max_length=100
    )

    description: Optional[str] = Field(
        "",
        description="A description of the collection, may contain markdown formatting",
        example="All HR policies and procedures"
    )

    sort: Optional[Sort] = Field(
        None,
        description="The sort of documents in the collection. Note that not all "
                    "API responses respect this and it is left as a frontend concern "
                    "to implement"
    )

    index: str = Field(
        ...,
        description="The position of the collection in the sidebar",
        example="P",
        min_length=1,
        max_length=2
    )

    color: Optional[str] = Field(
        ...,
        description="A color representing the collection, this is used to help "
                    "make collections more identifiable in the UI. It should be in "
                    "HEX format including the #",
        example="#123123",
        pattern="^#[0-9a-fA-F]{6}$"
    )

    icon: Optional[str] = Field(
        None,
        description="A string that represents an icon in the outline-icons package",
        example="folder"
    )

    permission: Permission = Field(
        ...,
        description="Access permissions for this collection"
    )

    sharing: bool = Field(
        False,
        description="Whether public document sharing is enabled in this collection",
        example=False
    )

    created_at: datetime = Field(
        ...,
        alias='createdAt',
        description="The date and time that this object was created",
        read_only=True,
        example="2023-01-15T09:30:00Z"
    )

    updated_at: datetime = Field(
        ...,
        alias='updatedAt',
        description="The date and time that this object was last changed",
        read_only=True,
        example="2023-06-20T14:25:00Z"
    )

    deleted_at: Optional[datetime] = Field(
        None,
        alias='deletedAt',
        description="The date and time that this object was deleted",
        read_only=True,
        example=None
    )

    archived_at: Optional[datetime] = Field(
        None,
        alias='archivedAt',
        description="The date and time that this object was archived",
        read_only=True,
        example=None
    )

    archived_by: Optional[User] = Field(
        None,
        alias='archivedBy',
        description="User who archived this collection",
        read_only=True
    )


class CollectionResponse(Response):
    data: Optional[Collection] = Field(None)


class CollectionListResponse(Response):
    data: Optional[List[Collection]] = Field([])

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..const import HEX_COLOR_PATTERN
from .response import Permission, Response, Sort
from .user import User, UserMembership


class Collection(BaseModel):
    """
    Represents a collection of documents in the system.

    Collections are used to organize documents into groups with shared permissions
    and settings. They appear in the sidebar navigation.
    """

    id: UUID = Field(
        ...,
        json_schema_extra={
            "description": "Unique identifier for the object",
            "example": "550e8400-e29b-41d4-a716-446655440000",
            "readOnly": True,
        },
    )

    url_id: str = Field(
        ...,
        alias="urlId",
        min_length=8,
        max_length=16,
        json_schema_extra={
            "description": "A short unique identifier that can be used to identify the "
            "collection instead of the UUID",
            "example": "hDYep1TPAM",
            "readOnly": True,
        },
    )

    name: str = Field(
        ...,
        max_length=100,
        json_schema_extra={
            "description": "The name of the collection",
            "example": "Human Resources",
        },
    )

    description: str | None = Field(
        "",
        json_schema_extra={
            "description": "A description of the collection, may contain markdown formatting",
            "example": "All HR policies and procedures",
        },
    )

    sort: Sort | None = Field(
        None,
        json_schema_extra={
            "description": "The sort of documents in the collection. Note that not all "
            "API responses respect this and it is left as a frontend concern "
            "to implement"
        },
    )

    index: str = Field(
        ...,
        min_length=1,
        max_length=10,
        json_schema_extra={
            "description": "The position of the collection in the sidebar",
            "example": "P",
        },
    )

    color: str | None = Field(
        ...,
        pattern=HEX_COLOR_PATTERN,
        json_schema_extra={
            "description": "A color representing the collection, this is used to help "
            "make collections more identifiable in the UI. It should be in "
            "HEX format including the #",
            "example": "#123123",
        },
    )

    icon: str | None = Field(
        None,
        json_schema_extra={
            "description": "A string that represents an icon in the outline-icons package",
            "example": "folder",
        },
    )

    permission: Permission | None = Field(
        None, description="Access permissions for this collection"
    )

    sharing: bool = Field(
        False,
        json_schema_extra={
            "description": "Whether public document sharing is enabled in this collection",
            "example": False,
        },
    )

    created_at: datetime = Field(
        ...,
        alias="createdAt",
        json_schema_extra={
            "description": "The date and time that this object was created",
            "example": "2023-01-15T09:30:00Z",
            "readOnly": True,
        },
    )

    updated_at: datetime = Field(
        ...,
        alias="updatedAt",
        json_schema_extra={
            "description": "The date and time that this object was last changed",
            "example": "2023-06-20T14:25:00Z",
            "readOnly": True,
        },
    )

    deleted_at: datetime | None = Field(
        None,
        alias="deletedAt",
        json_schema_extra={
            "description": "The date and time that this object was deleted",
            "example": None,
            "readOnly": True,
        },
    )

    archived_at: datetime | None = Field(
        None,
        alias="archivedAt",
        json_schema_extra={
            "description": "The date and time that this object was archived",
            "example": None,
            "readOnly": True,
        },
    )

    archived_by: User | None = Field(
        None,
        alias="archivedBy",
        json_schema_extra={
            "description": "User who archived this collection",
            "readOnly": True,
        },
    )


class NavigationNode(BaseModel):
    """
    Represents a document as a navigation node with its children (also represented as navigation nodes)
    """

    id: UUID = Field(
        ...,
        json_schema_extra={
            "description": "Unique identifier for the object",
            "example": "550e8400-e29b-41d4-a716-446655440000",
            "readOnly": True,
        },
    )
    url: str
    title: str
    children: list["NavigationNode"] = Field(default_factory=list)
    icon: str | None = Field(None)
    color: str | None = Field(
        None,
        pattern=HEX_COLOR_PATTERN,
        json_schema_extra={
            "description": "Document's icon color in hex format",
            "example": "#FF5733",
            "readOnly": True,
        },
    )


class CollectionResponse(Response):
    data: Collection | None = Field(None)


class CollectionNavigationResponse(Response):
    data: list[NavigationNode]


class CollectionListResponse(Response):
    data: list[Collection] = Field(default_factory=list)


class CollectionUserResponse(Response):
    data: UserMembership | None = Field(None)

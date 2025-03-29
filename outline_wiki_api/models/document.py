
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from .user import User
from .response import Response


class DocumentTasks(BaseModel):
    completed: int
    total: int


class Document(BaseModel):
    """
    Represents a document in the system, containing rich text content and metadata.

    Documents are the primary content type, supporting Markdown formatting,
    collaboration features, and version history.
    """
    id: UUID = Field(
        ...,
        description="Unique identifier for the object",
        read_only=True,
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    collection_id: UUID = Field(
        ...,
        alias='collectionId',
        description="Identifier for the associated collection",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    parent_document_id: Optional[UUID] = Field(
        None,
        alias='parentDocumentId',
        description="Identifier for the document this is a child of, if any",
        example="550e8400-e29b-41d4-a716-446655440001"
    )
    title: str = Field(
        ...,
        description="The title of the document",
        example="🎉 Welcome to Acme Inc"
    )
    full_width: bool = Field(
        False,
        alias='fullWidth',
        description="Whether this document should be displayed in a full-width view",
        example=True
    )
    emoji: Optional[str] = Field(
        None,
        description="An emoji associated with the document",
        example="🎉"
    )
    text: str = Field(
        ...,
        description="The text content of the document, contains markdown formatting",
        example="# Welcome\nThis is a sample document with **markdown** support."
    )
    url: str
    url_id: str = Field(
        ...,
        alias='urlId',
        description="A short unique ID that can be used to identify the document "
                    "as an alternative to the UUID",
        example="hDYep1TPAM",
        min_length=8,
        max_length=16
    )
    collaborators: List[User] = Field(
        [],
        description="List of users who have collaborated on this document"
    )
    pinned: bool = Field(
        False,
        description="Whether this document is pinned in the collection",
        example=False
    )
    template: bool = Field(
        False,
        description="Whether this document is a template",
        example=False
    )
    template_id: Optional[UUID] = Field(
        None,
        alias='templateId',
        description="Unique identifier for the template this document was created from, if any",
        example="550e8400-e29b-41d4-a716-446655440002"
    )
    revision: int = Field(
        ...,
        description="A number that is auto incrementing with every revision of the document that is saved",
        read_only=True,
        example=12
    )
    created_at: datetime = Field(
        ...,
        alias='createdAt',
        description="The date and time that this object was created",
        read_only=True,
        example="2023-01-15T09:30:00Z"
    )
    created_by: User = Field(
        ...,
        alias='createdBy',
        description="User who created this document",
        read_only=True
    )
    updated_at: datetime = Field(
        ...,
        alias='updatedAt',
        description="The date and time that this object was last changed",
        read_only=True,
        example="2023-06-20T14:25:00Z"
    )
    updated_by: User = Field(
        ...,
        alias='updatedBy',
        description="User who last updated this document",
        read_only=True
    )
    published_at: Optional[datetime] = Field(
        None,
        alias='publishedAt',
        description="The date and time that this object was published",
        read_only=True,
        example="2023-02-01T10:15:00Z"
    )
    archived_at: Optional[datetime] = Field(
        None,
        alias='archivedAt',
        description="The date and time that this object was archived",
        read_only=True,
        example="2023-07-01T08:15:00Z"
    )
    deleted_at: Optional[datetime] = Field(
        None,
        alias='deletedAt',
        description="The date and time that this object was deleted",
        read_only=True,
        example=None
    )
    icon: Optional[str]
    color: Optional[str] = Field(
        None,
        description="Document's icon color in hex format",
        pattern="^#[0-9a-fA-F]{6}$",
        example="#FF5733"
    )
    tasks: Optional[DocumentTasks]
    last_viewed_at: Optional[datetime] = Field(
        None,
        description="The date and time that this object was viewed for the last time",
        alias="lastViewedAt"
    )
    is_collection_deleted: Optional[bool] = Field(
        None,
        alias="isCollectionDeleted"
    )
    insights_enabled: Optional[bool] = Field(
        None,
        alias="insightsEnabled"
    )


class DocumentListResponse(Response):
    data: Optional[List[Document]]


class DocumentSearchResult(BaseModel):
    ranking: float
    context: str
    document: Document


class DocumentSearchResultResponse(Response):
    data: Optional[List[DocumentSearchResult]]


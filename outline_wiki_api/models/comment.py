from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .response import Response
from .user import User


class Data(BaseModel):
    """
    Represents the data structure of a comment's content.
    """

    type: str = Field(
        ..., description="The type of the document node", examples=["doc"]
    )
    content: list[dict] = Field(
        ...,
        description="The content of the document node",
    )


class Comment(BaseModel):
    """
    Represents a comment in the system.
    """

    id: UUID = Field(
        ...,
        json_schema_extra={
            "description": "Unique identifier for the object",
            "example": "550e8400-e29b-41d4-a716-446655440000",
            "read_only": "true",
        },
    )
    parent_comment_id: UUID | None = Field(
        None,
        alias="parentCommentId",
        description="Identifier for the comment this is a child of, if any.",
        examples=["550e8400-e29b-41d4-a716-446655440001"],
    )
    data: Data = Field(
        ...,
        alias="data",
        description="The editor data representing this comment.",
    )
    document_id: UUID = Field(
        ...,
        alias="documentId",
        description="Identifier for the document this is related to.",
        examples=["550e8400-e29b-41d4-a716-446655440002"],
    )
    created_at: datetime = Field(
        ...,
        alias="createdAt",
        description="The date and time that this object was created",
        examples=["2023-01-15T09:30:00Z"],
        json_schema_extra={"read_only": "true"},
    )
    created_by: User = Field(
        ...,
        alias="createdBy",
        description="User who created this comment",
        json_schema_extra={"read_only": "true"},
    )
    updated_at: datetime | None = Field(
        ...,
        alias="updatedAt",
        description="The date and time that this object was last changed",
        examples=["2023-06-20T14:25:00Z"],
        json_schema_extra={"read_only": "true"},
    )
    updated_by: User | None = Field(
        None,
        alias="updatedBy",
        description="User who last updated this comment",
        json_schema_extra={"read_only": "true"},
    )
    anchor_text: str | None = Field(
        None,
        alias="anchorText",
        description="The document text that the comment is anchored to, only included if includeAnchorText=true.",
        json_schema_extra={"read_only": "true"},
    )


class CommentResponse(Response):
    """A single Comment object response"""

    data: Comment | None = Field(None)


class CommentListResponse(Response):
    """A Collection of the Comment objects response"""

    data: list[Comment] | None = Field(None)

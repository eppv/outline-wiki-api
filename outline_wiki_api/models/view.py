"""
Data structures for View resource information and responses
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from .user import User
from .response import Response


class View(BaseModel):
    """
    Represents a compressed record of an individual user's views of a
    document. Individual views are not recorded but a first, last and total
    is kept per user.
    """

    id: UUID = Field(
        ..., json_schema_extra={"description": "Unique identifier for the object"}
    )
    document_id: UUID = Field(
        ...,
        alias="documentId",
        json_schema_extra={"description": "Identifier for the associated document"},
    )

    first_viewed_at: datetime = Field(
        ...,
        alias="firstViewedAt",
        json_schema_extra={
            "description": "When the document was first viewed by the user"
        },
    )

    last_viewed_at: datetime = Field(
        ...,
        alias="lastViewedAt",
        json_schema_extra={
            "description": "When the document was last viewed by the user"
        },
    )

    count: int | None = Field(
        None,
        json_schema_extra={
            "description": "The number of times the user has viewed the document"
        },
    )

    user: User | None = Field(
        None, json_schema_extra={"description": "User who viewed the document"}
    )


class ViewResponse(Response):
    data: View | None = None


class ViewListResponse(Response):
    data: list[View] | None = Field(default=[])

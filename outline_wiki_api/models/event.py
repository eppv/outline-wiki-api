"""
Data structures for Event resource information and responses
"""

from datetime import datetime
from typing import Optional, Union, Any
from uuid import UUID
from pydantic import BaseModel, Field
from .response import Response
from .user import User


class Event(BaseModel):
    """
    `Event` represents an artifact of an action. Whether it is creating a user,
    editing a document, changing permissions, or any other action – an event
    is created that can be used as an audit trail or activity stream.
    """
    id: UUID = Field(
        ...,
        json_schema_extra={
            "description": "Unique identifier for the object",
            "read_only": True
        }
    )

    name: str = Field(
        ...,
        json_schema_extra={
            "description": "Name of the event",
            "read_only": True
        }
    )

    model_id: Optional[UUID] = Field(
        ...,
        alias="modelId",
        json_schema_extra={
            "description": "Identifier for the object this event is associated with when it is not one of document, collection, or user",
            "read_only": True
        }
    )

    actor_id: UUID = Field(
        ...,
        alias="actorId",
        json_schema_extra={
            "description": "The ID of the user that performed the action",
            "read_only": True
        }
    )

    user_id: Optional[UUID] = Field(
        ...,
        alias="userId",
        json_schema_extra={
            "description": "The ID of the user that performed the action (duplicated)",
            "read_only": True
        }
    )

    collection_id: Optional[UUID] = Field(
        ...,
        alias="collectionId",
        json_schema_extra={
            "description": "The ID of the collection that the event is associated with",
            "read_only": True
        }
    )

    document_id: Optional[UUID] = Field(
        ...,
        alias="documentId",
        json_schema_extra={
            "description": "The ID of the document that the event is associated with",
            "read_only": True
        }
    )

    actor: User = Field(
        ...,
        alias="actor",
        json_schema_extra={
            "description": "The user that performed the action",
            "read_only": True
        }
    )

    created_at: datetime = Field(
        ...,
        alias="createdAt",
        json_schema_extra={
            "description": "The date and time the event was created",
            "read_only": True
        }
    )

    data: Optional[Any] = Field(
        None,
        alias="data",
        json_schema_extra={
            "description": "Additional unstructured data associated with the event",
            "read_only": True
        }
    )



class EventListResponse(Response):
    data: Optional[list[Event]] = Field(default=[])

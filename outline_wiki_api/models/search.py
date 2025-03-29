from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    offset: int
    limit: int


class Sort(BaseModel):
    field: str = Field(
        ...,
        description="Field to sort documents by",
        example="title"
    )
    direction: Literal["asc", "desc"] = Field(
        "asc",
        description="Sort direction - ascending or descending",
        example="desc"
    )


class SearchResult(BaseModel):
    id: UUID
    query: str
    answer: str
    source: str
    created_at: datetime = Field(..., alias="createdAt")

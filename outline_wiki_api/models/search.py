from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    offset: int
    limit: int


class Sorting(BaseModel):
    field: str
    direction: Literal["asc", "desc"] = "asc"


class SearchResult(BaseModel):
    id: UUID
    query: str
    answer: str
    source: str
    created_at: datetime = Field(..., alias="createdAt")

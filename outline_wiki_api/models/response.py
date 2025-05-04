"""
Basic API data structures
"""

from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any, Literal


class Period(str, Enum):
    """Available date filter options"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Policy(BaseModel):
    """
    Most API resources have associated "policies", these objects describe the
    current API keys authorized actions related to an individual resource. It
    should be noted that the policy "id" is identical to the resource it is
    related to, policies themselves do not have unique identifiers.

    For most usecases of the API, policies can be safely ignored. Calling
    unauthorized methods will result in the appropriate response code – these can
    be used in an interface to adjust which elements are visible.
    """
    id: UUID
    abilities: Dict


class Sort(BaseModel):
    """
    Sorting data model used to configure the order of results obtained in methods that return arrays.
    """
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


class Pagination(BaseModel):
    """
    Pagination data model used to configure the number of results obtained in methods that return arrays.
    """
    offset: int
    limit: int
    next_path: Optional[str] = Field(
        None,
        alias="nextPath"
    )
    total: Optional[int] = None


class Response(BaseModel):
    """
    Base Outline API response data structure
    """
    status: int
    ok: bool
    data: Optional[Any] = None
    pagination: Optional[Pagination] = None
    policies: Optional[List[Policy]] = None


class Permission(str, Enum):
    """Available permission options for collections and documents"""
    READ = 'read'
    READ_WRITE = 'read_write'

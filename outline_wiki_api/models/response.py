
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any, Literal


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
    offset: int
    limit: int
    next_path: Optional[str] = Field(
        None,
        alias="nextPath"
    ),
    total: Optional[int]


class Response(BaseModel):
    status: int
    ok: bool
    data: Optional[Any]
    pagination: Optional[Pagination]
    policies: Optional[List[Policy]]





from typing import Optional, List, Dict
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.collection import CollectionListResponse


class Collections(Resources):
    """
    `Collections` represent grouping of documents in the knowledge base, they
    offer a way to structure information in a nested hierarchy and a level
    at which read and write permissions can be granted to individual users or
    groups of users.
    """
    _path: str = '/collections'

    def list(
            self,
            query: Optional[str] = None,
            status_filter: Optional[List[str]] = None,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sort] = None
    ) -> CollectionListResponse:
        """
        List all collections

        Args:
            query: If set, will filter the results by collection name.
            status_filter: Optional statuses to filter by
            pagination: Pagination options
            sorting: Sorting options

        Returns:
            Dict: Contains data (collections), policies, and pagination info
        """
        data = {}
        if query:
            data["query"] = query
        if status_filter:
            data["statusFilter"] = status_filter
        if pagination:
            data.update(pagination.dict())
        if sorting:
            data.update(sorting.dict())

        response = self.post("list", data=data)

        return CollectionListResponse(**response.json())


from typing import Optional, List, Dict, Union
from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.collection import CollectionResponse, CollectionListResponse, CollectionNavigationResponse


class Collections(Resources):
    """
    `Collections` represent grouping of documents in the knowledge base, they
    offer a way to structure information in a nested hierarchy and a level
    at which read and write permissions can be granted to individual users or
    groups of users.

    Methods:
        info: Retrieve a collection
        documents: Retrieve a collections document structure
        list: List all collections

    """
    _path: str = '/collections'

    def info(self, collection_id: Union[str, UUID]) -> CollectionResponse:
        """
        Retrieve a collection

        Args:
            collection_id: Unique identifier for the collection

        Returns:
            CollectionResponse:
                A response containing a Collection object
        """

        data = {"id": str(collection_id)}
        response = self.post("info", data=data)
        return CollectionResponse(**response.json())

    def documents(self, collection_id: Union[str, UUID]):
        """
        Retrieve a collections document structure (as nested navigation nodes)

        Args:
            collection_id: Unique identifier for the collection

        Returns:
            CollectionNavigationResponse:
                A response containing a nested structure of document navigation nodes
        """
        data = {"id": str(collection_id)}
        response = self.post("documents", data=data)
        return CollectionNavigationResponse(**response.json())

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
            CollectionListResponse: A response containing an array of Collection objects
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

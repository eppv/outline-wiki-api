from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Permission, Sort
from ..models.collection import (
    CollectionResponse,
    CollectionListResponse,
    CollectionNavigationResponse,
)


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

    _path: str = "/collections"

    def info(self, collection_id: str | UUID) -> CollectionResponse:
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

    def documents(self, collection_id: str | UUID):
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
        query: str | None = None,
        status_filter: list[str] | None = None,
        pagination: Pagination | None = None,
        sorting: Sort | None = None,
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
            data.update(pagination)
        if sorting:
            data.update(sorting)

        response = self.post("list", data=data)

        return CollectionListResponse(**response.json())

    def create(
        self,
        name: str,
        description: str | None,
        permission: Permission | None,
        icon: str | None,
        color: str | None,
        sharing: bool | None,
    ):
        """
        Create a new collection

        Args:
            name: The name of the collection
            description: The description of the collection
            permission: The permission of the collection
            icon: The icon of the collection
            color: The color of the collection
            sharing: Whether the collection is shared

        Returns:
            Collection: The created collection
        """

        data = {}
        if description:
            data["description"] = description
        if permission:
            data["permission"] = permission
        if icon:
            data["icon"] = icon
        if color:
            data["color"] = color
        if sharing:
            data["sharing"] = sharing

        response = self.post("create", data=data)

        return CollectionResponse(**response.json())

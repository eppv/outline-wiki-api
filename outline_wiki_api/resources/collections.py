from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Permission, Sort
from ..models.collection import (
    CollectionResponse,
    CollectionListResponse,
    CollectionNavigationResponse,
    CollectionUserResponse,
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
        create: Create a collection
        update: Update a collection
        delete: Delete a collection
        add_user: Add a user to a collection
        remove_user: Remove a user from a collection
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
            query: If set, will filter the results by collection name
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
        description: str | None = None,
        permission: Permission | None = None,
        icon: str | None = None,
        color: str | None = None,
        sharing: bool = False,
    ):
        """
        Create a new collection

        Args:
            name: The name of the collection
            description: A brief description of the collection, markdown supported
            permission: The permission of the collection
            icon: A string that represents an icon in the outline-icons package or an emoji
            color: A hex color code for the collection icon
            sharing: Whether public sharing of documents is allowed

        Returns:
            Collection: The created collection
        """

        data = {"name": name}
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

    def update(
        self,
        collection_id: UUID | str,
        name: str | None = None,
        description: str | None = None,
        permission: Permission | None = None,
        icon: str | None = None,
        color: str | None = None,
        sharing: bool | None = None,
    ):
        """
        Update a collection

        Args:
            id: The id of the collection
            name: The name of the collection
            description: A brief description of the collection, markdown supported
            permission: The permission of the collection
            icon: A string that represents an icon in the outline-icons package or an emoji
            color: A hex color code for the collection icon
            sharing: Whether public sharing of documents is allowed

        Returns:
            Collection: The updated collection
        """

        data = {"id": str(collection_id)}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if permission:
            data["permission"] = permission
        if icon:
            data["icon"] = icon
        if color:
            data["color"] = color
        if sharing is not None:
            data["sharing"] = sharing

        response = self.post("update", data=data)

        return CollectionResponse(**response.json())

    def delete(self, collection_id: UUID | str):
        """
        Delete a collection

        This method allows you to delete a collection.

        Args:
            id: The id of the collection

        Returns:
            bool: True if the collection was deleted, False otherwise
        """
        response = self.post("delete", data={"id": str(collection_id)})
        return response.json()["success"]

    def add_user(
        self,
        collection_id: UUID | str,
        user_id: UUID | str,
        permission: Permission | str | None = None,
    ) -> CollectionResponse:
        """
        Add a collection user

        This method allows you to add a user membership to the specified
        collection.

        Args:
            id: The id of the collection
            email: The id of the user to add
            permission: The permission to grant the user

        Returns:
            Collection: The updated collection
        """

        data = {"id": str(collection_id), "userId": str(user_id)}
        if permission:
            data["permission"] = permission

        response = self.post("add_user", data=data)

        return CollectionUserResponse(**response.json())

    def remove_user(
        self,
        collection_id: UUID | str,
        user_id: UUID | str,
    ) -> bool:
        """
        Remove a collection user

        This method allows you to remove a user membership from the specified
        collection

        Args:
            id: The id of the collection
            email: The id of the user to remove

        Returns:
            success: Status of the operation
        """

        data = {"id": str(collection_id), "userId": str(user_id)}

        response = self.post("remove_user", data=data)

        return response.json()["success"]

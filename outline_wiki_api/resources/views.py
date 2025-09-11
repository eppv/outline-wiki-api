"""
Classes for Views resources group

Classes:
    Views: Views resources method group main class
"""

from typing import Optional, Union
from uuid import UUID
from .base import Resources
from ..models.view import ViewResponse, ViewListResponse


class Views(Resources):
    """
    `Views` represent a compressed record of an individual users views of a
    document. Individual views are not recorded but a first, last and total
    is kept per user.

    Methods:
        list: List all views for a document
        create: Creates a view for a document (not recommended to use outside of the UI, but still implemented for testing purposes)
    """
    _path: str = '/views'

    def list(self, document_id:  Union[str, UUID]):
        """
        List all users that have viewed a document and the overall view

        Args:
            document_id: The id of the document to list views for

        Returns:
            ViewListResponse: a response object which contains a View object as data
        """
        data = {"documentId": str(document_id)}
        response = self.post("list", data=data)
        return ViewListResponse(**response.json())

    def create(self, document_id: Union[str, UUID]):
        """
        Creates a new view for a document. This is documented in the interests
        of thoroughness however it is recommended that views are not created from
        outside of the Outline UI.

        Args:
            document_id: The id of the document to create a view for

        Returns:
            ViewResponse: The created view response object
        """
        data = {"documentId": str(document_id)}
        response = self.post("create", data=data)
        return ViewResponse(**response.json())

import json
from io import BufferedReader
from typing import Optional, Dict, Union, Literal
from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.document import (
    Document,
    DocumentListResponse,
    DocumentSearchResultResponse
)


class Documents(Resources):
    """
    `Documents` are what everything else revolves around. A document represents
    a single page of information and always returns the latest version of the
    content. Documents are stored in [Markdown](https://spec.commonmark.org/)
    formatting.
    """
    _path: str = "/documents"

    def info(self, doc_id: str, share_id: Optional[UUID] = None) -> Document:
        """
        Retrieve a document by ID or shareId

        Args:
            doc_id: Unique identifier for the document (UUID or urlId)
            share_id: Optional share identifier

        Returns:
            Document: The requested document
        """
        data = {"id": doc_id}
        if share_id:
            data["shareId"] = str(share_id)
        response = self.post("info", data=data)
        print(json.dumps(response.json()["data"], indent=4))
        return Document(**response.json()["data"])

    def import_file(
            self,
            file: BufferedReader,
            collection_id: Union[UUID, str],
            parent_document_id: Optional[Union[UUID, str]] = None,
            template: bool = False,
            publish: bool = False
    ) -> Document:
        """
        Import a file as a new document

        Args:
            file: File object to import
            collection_id: Target collection ID
            parent_document_id: Optional parent document ID
            template: Whether to create as template
            publish: Whether to publish immediately

        Returns:
            Document: The created document
        """
        files = {"file": file}
        data = {
            "collectionId": str(collection_id),
            "template": template,
            "publish": publish
        }
        if parent_document_id:
            data["parentDocumentId"] = str(parent_document_id)

        response = self.post("import", data=data, files=files)
        return Document(**response["data"])

    def export(self, doc_id: str) -> str:
        """
        Export document as markdown

        Args:
            doc_id: Document ID (UUID or urlId)

        Returns:
            str: Document content in Markdown format
        """
        response = self.post("export", data={"id": doc_id})
        return response.json()["data"]

    def list(
            self,
            collection_id: Optional[Union[UUID, str]] = None,
            user_id: Optional[Union[UUID, str]] = None,
            backlink_document_id: Optional[Union[UUID, str]] = None,
            parent_document_id: Optional[Union[UUID, str]] = None,
            template: Optional[bool] = None,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sort] = None
    ) -> DocumentListResponse:
        """
        List all published and user's draft documents

        Returns:
            Dict: Contains data (documents), policies, and pagination info
        """
        data = {}
        if collection_id:
            data["collectionId"] = str(collection_id)
        if user_id:
            data["userId"] = str(user_id)
        if backlink_document_id:
            data["backlinkDocumentId"] = str(backlink_document_id)
        if parent_document_id:
            data["parentDocumentId"] = str(parent_document_id)
        if template is not None:
            data["template"] = template
        if pagination:
            data.update(pagination.dict())
        if sorting:
            data.update(sorting.dict())

        response = self.post("list", data=data)
        return DocumentListResponse(**response.json())

    def create(
            self,
            title: str,
            collection_id: Union[UUID, str],
            text: Optional[str] = None,
            parent_document_id: Optional[Union[UUID, str]] = None,
            template_id: Optional[Union[UUID, str]] = None,
            template: bool = False,
            publish: bool = False
    ) -> Document:
        """
        Create a new document

        Args:
            title: Document title
            collection_id: Target collection ID
            text: Document content (markdown)
            parent_document_id: Optional parent document ID
            template_id: Template to base document on
            template: Whether to create as template
            publish: Whether to publish immediately

        Returns:
            Document: The created document
        """
        data = {
            "title": title,
            "collectionId": str(collection_id),
            "template": template,
            "publish": publish
        }
        if text:
            data["text"] = text
        if parent_document_id:
            data["parentDocumentId"] = str(parent_document_id)
        if template_id:
            data["templateId"] = str(template_id)

        response = self.post("create", data=data)
        return Document(**response.json()["data"])

    def search(
            self,
            query: str,
            user_id: Optional[Union[UUID, str]] = None,
            collection_id: Optional[Union[UUID, str]] = None,
            document_id: Optional[Union[UUID, str]] = None,
            status_filter: Optional[Literal["draft", "archived", "published"]] = None,
            date_filter: Optional[Literal["day", "week", "month", "year"]] = None,
            pagination: Optional[Pagination] = None
    ) -> DocumentSearchResultResponse:
        """
        Search documents with keywords

        Returns:
            Response: Contains search results, policies, and pagination info
        """
        data = {"query": query}
        if user_id:
            data["userId"] = str(user_id)
        if collection_id:
            data["collectionId"] = str(collection_id)
        if document_id:
            data["documentId"] = str(document_id)
        if status_filter:
            data["statusFilter"] = status_filter
        if date_filter:
            data["dateFilter"] = date_filter
        if pagination:
            data.update(pagination.dict())

        response = self.post("search", data=data)

        return DocumentSearchResultResponse(**response.json())

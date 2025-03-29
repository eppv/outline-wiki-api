import json
from io import BufferedReader
from typing import Optional, Dict
from uuid import UUID
from .base import Resources
from ..models.document import Document
from ..models.search import Pagination, Sorting


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
            collection_id: UUID,
            parent_document_id: Optional[UUID] = None,
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
            collection_id: Optional[UUID] = None,
            user_id: Optional[UUID] = None,
            backlink_document_id: Optional[UUID] = None,
            parent_document_id: Optional[UUID] = None,
            template: Optional[bool] = None,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sorting] = None
    ) -> Dict:
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
        return response.json()["data"]

    def create(self, document: Document):
        raise NotImplementedError

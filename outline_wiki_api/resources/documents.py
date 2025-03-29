
from io import BufferedReader
from typing import Optional
from uuid import UUID
from .base import Resources
from ..models.document import Document


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
        return Document(**response["data"])

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
        response = self.post("export", data={"id": id})
        return response["data"]

    def list(self,
             offset: int = 1,
             limit: int = 25,
             sort: str = 'updatedAt',
             direction: str = 'DESC',
             collection_id: Optional[str] = None,
             user_id: str = '',
             backlink_document_id: Optional[str] = None,
             parent_document_id: Optional[str] = None,
             template: bool = False):
        method = f'{self._path}.list'
        data = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "direction": direction,
            "collectionId": collection_id,
            "userId": user_id if user_id else f"{self._client.auth.user_id}",
            "template": template
        }

        data.update({"backlinkDocumentId": backlink_document_id}) if backlink_document_id else None
        data.update({"parentDocumentId": parent_document_id}) if parent_document_id else None

        return self.client.post(
            method=method,
            data=data
        )

    def create(self, document: Document):
        method = f'{self._path}.create'
        data = {
            "title": document.title,
            "text": document.text,
            "collectionId": document.collection_id,
            "parentDocumentId": document.parent_document_id,
            "template": document.template,
            "publish": document.publish
        }

        data.update({"templateId": document.template_id}) if document.template else None

        return self.client.post(
            method=method,
            data=data
        )

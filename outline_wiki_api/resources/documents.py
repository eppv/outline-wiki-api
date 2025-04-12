
from io import BufferedReader
from typing import Optional, Dict, Union, Literal, Tuple
from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.document import (
    Document,
    DocumentResponse,
    DocumentListResponse,
    DocumentSearchResultResponse,
    DocumentAnswerResponse,
    DocumentMoveResponse,
    DocumentUsersResponse,
    DocumentMembershipsResponse
)
from ..utils import get_file_object_for_import


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
            The requested document
        """
        data = {"id": doc_id}
        if share_id:
            data["shareId"] = str(share_id)
        response = self.post("info", data=data)
        return DocumentResponse(**response.json()).data

    def import_file(
            self,
            file: Union[str, Tuple],
            collection_id: Union[UUID, str],
            parent_document_id: Optional[Union[UUID, str]] = None,
            template: bool = False,
            publish: bool = False
    ) -> Document:
        """
        Import a file as a new document

        Args:
            file: Path to a file OR File Object for import (Plain text, markdown, docx, csv, tsv, and html format are supported.)
            collection_id: Target collection ID
            parent_document_id: Optional parent document ID
            template: Whether to create as template
            publish: Whether to publish immediately

        Returns:
            The created document
        """
        if isinstance(file, str):
            file_object = get_file_object_for_import(file)
        else:
            file_object = file
        files = {
            "file": file_object,
            "collectionId": (None, str(collection_id)),
        }
        if parent_document_id:
            files["parentDocumentId"] = (None, str(parent_document_id))
        if template:
            files["template"] = (None, "true")
        else:
            files["template"] = (None, "false")
        if publish:
            files["publish"] = (None, "true")
        else:
            files["publish"] = (None, "false")

        response = self.post("import", files=files)
        return DocumentResponse(**response.json()).data

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

    def drafts(
            self,
            collection_id: Optional[Union[UUID, str]] = None,
            date_filter: Optional[Literal["day", "week", "month", "year"]] = None,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sort] = None
    ) -> DocumentListResponse:
        """
        List all draft documents belonging to the current user

        Args:
            collection_id: Optional collection to filter by
            date_filter: Filter by update date
            pagination: Pagination parameters
            sorting: Sorting parameters

        Returns:
            DocumentListResponse: List of draft documents
        """
        data = {}
        if collection_id:
            data["collectionId"] = str(collection_id)
        if date_filter:
            data["dateFilter"] = date_filter
        if pagination:
            data.update(pagination.dict())
        if sorting:
            data.update(sorting.dict())

        response = self.post("drafts", data=data)
        return DocumentListResponse(**response.json())

    def viewed(
            self,
            pagination: Optional[Pagination] = None,
            sorting: Optional[Sort] = None
    ) -> DocumentListResponse:
        """
        List all recently viewed documents

        Args:
            pagination: Pagination parameters
            sorting: Sorting parameters

        Returns:
            DocumentListResponse: List of recently viewed documents
        """
        data = {}
        if pagination:
            data.update(pagination.dict())
        if sorting:
            data.update(sorting.dict())

        response = self.post("viewed", data=data)
        return DocumentListResponse(**response.json())

    def answer_question(
            self,
            query: str,
            user_id: Optional[Union[UUID, str]] = None,
            collection_id: Optional[Union[UUID, str]] = None,
            document_id: Optional[Union[UUID, str]] = None,
            status_filter: Optional[Literal["draft", "archived", "published"]] = None,
            date_filter: Optional[Literal["day", "week", "month", "year"]] = None
    ) -> DocumentAnswerResponse:
        """
        Query documents with natural language

        Args:
            query: The question to ask
            user_id: Filter by user
            collection_id: Filter by collection
            document_id: Filter by document
            status_filter: Filter by status
            date_filter: Filter by date

        Returns:
            DocumentAnswerResponse: Answer and related documents
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

        response = self.post("answerQuestion", data=data)
        return DocumentAnswerResponse(**response.json())

    def templatize(self, doc_id: Union[UUID, str]) -> Document:
        """
        Create a template from a document

        Args:
            doc_id: Document ID to templatize

        Returns:
            Document: The created template
        """
        response = self.post("templatize", data={"id": str(doc_id)})
        return Document(**response.json()["data"])

    def unpublish(self, doc_id: Union[UUID, str]) -> Document:
        """
        Unpublish a document

        Args:
            doc_id: Document ID to unpublish

        Returns:
            Document: The unpublished document
        """
        response = self.post("unpublish", data={"id": str(doc_id)})
        return Document(**response.json()["data"])

    def move(
            self,
            doc_id: Union[UUID, str],
            collection_id: Optional[Union[UUID, str]] = None,
            parent_document_id: Optional[Union[UUID, str]] = None
    ) -> DocumentMoveResponse:
        """
        Move a document to a new location

        Args:
            doc_id: Document ID to move
            collection_id: Target collection ID
            parent_document_id: Target parent document ID

        Returns:
            DocumentMoveResponse: Updated documents and collections
        """
        data = {"id": str(doc_id)}
        if collection_id:
            data["collectionId"] = str(collection_id)
        if parent_document_id:
            data["parentDocumentId"] = str(parent_document_id)

        response = self.post("move", data=data)
        return DocumentMoveResponse(**response.json()["data"])

    def archive(self, doc_id: Union[UUID, str]) -> Document:
        """
        Archive a document

        Args:
            doc_id: Document ID to archive

        Returns:
            Document: The archived document
        """
        response = self.post("archive", data={"id": str(doc_id)})
        return Document(**response.json()["data"])

    def restore(
            self,
            doc_id: Union[UUID, str],
            revision_id: Optional[Union[UUID, str]] = None
    ) -> Document:
        """
        Restore a document

        Args:
            doc_id: Document ID to restore
            revision_id: Optional revision ID to restore to

        Returns:
            Document: The restored document
        """
        data = {"id": str(doc_id)}
        if revision_id:
            data["revisionId"] = str(revision_id)

        response = self.post("restore", data=data)
        return Document(**response.json()["data"])

    def delete(
            self,
            doc_id: Union[UUID, str],
            permanent: bool = False
    ) -> bool:
        """
        Delete a document

        Args:
            doc_id: Document ID to delete
            permanent: Whether to permanently delete

        Returns:
            bool: Success status
        """
        response = self.post("delete", data={
            "id": str(doc_id),
            "permanent": permanent
        })
        return response.json()["success"]

    def users(
            self,
            doc_id: Union[UUID, str],
            query: Optional[str] = None
    ) -> DocumentUsersResponse:
        """
        List all users with access to a document

        Args:
            doc_id: Document ID
            query: Optional filter by user name

        Returns:
            DocumentUsersResponse: List of users with access
        """
        data = {"id": str(doc_id)}
        if query:
            data["query"] = query

        response = self.post("users", data=data)
        return DocumentUsersResponse(**response.json())

    def memberships(
            self,
            doc_id: Union[UUID, str],
            query: Optional[str] = None
    ) -> DocumentMembershipsResponse:
        """
        List users with direct membership to a document

        Args:
            doc_id: Document ID
            query: Optional filter by user name

        Returns:
            DocumentMembershipsResponse: List of direct memberships
        """
        data = {"id": str(doc_id)}
        if query:
            data["query"] = query

        response = self.post("memberships", data=data)
        return DocumentMembershipsResponse(**response.json())

    def add_user(
            self,
            doc_id: Union[UUID, str],
            user_id: Union[UUID, str],
            permission: Optional[str] = None
    ) -> Dict:
        """
        Add a user to a document

        Args:
            doc_id: Document ID
            user_id: User ID to add
            permission: Optional permission level

        Returns:
            Dict: Updated users and memberships
        """
        data = {
            "id": str(doc_id),
            "userId": str(user_id)
        }
        if permission:
            data["permission"] = permission

        response = self.post("add_user", data=data)
        return response.json()["data"]

    def remove_user(
            self,
            doc_id: Union[UUID, str],
            user_id: Union[UUID, str]
    ) -> bool:
        """
        Remove a user from a document

        Args:
            doc_id: Document ID
            user_id: User ID to remove

        Returns:
            bool: Success status
        """
        response = self.post("remove_user", data={
            "id": str(doc_id),
            "userId": str(user_id)
        })
        return response.json()["success"]

    

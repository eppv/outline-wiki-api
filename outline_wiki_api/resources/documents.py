
from typing import Optional, Dict, Union, Literal, Tuple
from uuid import UUID
from .base import Resources
from ..models.response import (
    Pagination,
    Sort,
    Period,
    Permission
)
from ..models.document import (
    DocumentResponse,
    DocumentListResponse,
    DocumentSearchResultResponse,
    DocumentAnswerResponse,
    DocumentMoveResponse,
    DocumentUsersResponse,
    DocumentMembershipsResponse,
    DocumentStatus
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

    def info(self, doc_id: Union[str, UUID], share_id: Optional[Union[str, UUID]] = None) -> DocumentResponse:
        """
        Retrieve a document by ID or shareId

        Args:
            doc_id: Unique identifier for the document (UUID or urlId)
            share_id: Optional share identifier

        Returns:
            DocumentResponse: The response object for the requested document
        """
        data = {"id": str(doc_id)}
        if share_id:
            data["shareId"] = str(share_id)
        response = self.post("info", data=data)
        return DocumentResponse(**response.json())

    def import_file(
            self,
            file: Union[str, Tuple],
            collection_id: Union[UUID, str],
            parent_document_id: Optional[Union[UUID, str]] = None,
            template: bool = False,
            publish: bool = False
    ) -> DocumentResponse:
        """
        Import a file as a new document

        Args:
            file: Path to a file OR File Object for import (Plain text, markdown, docx, csv, tsv, and html format are supported.)
            collection_id: Target collection ID
            parent_document_id: Optional parent document ID
            template: Whether to create as template
            publish: Whether to publish immediately

        Returns:
            DocumentResponse: The response object for the created document
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
        return DocumentResponse(**response.json())

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

        Args:
            collection_id: Optionally filter to a specific collection
            user_id: Optionally filter to a specific user
            backlink_document_id: Optionally filter to a specific document in a backlinks
            parent_document_id: Optionally filter to a specific parent document
            template: Optionally filter to only templates
            pagination: Custom pagination (default: offset=0, limit=25)
            sorting: Custom sorting order (takes `Sort` object)

        Returns:
            DocumentListResponse: Contains data (documents), policies, and pagination info
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
    ) -> DocumentResponse:
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
            DocumentResponse: The response object for the created document
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
        return DocumentResponse(**response.json())

    def update(
            self,
            doc_id: Union[UUID, str],
            title: Optional[str] = None,
            text: Optional[str] = None,
            append: bool = False,
            publish: bool = False,
            done: bool = False
    ) -> DocumentResponse:
        """
        Args:
            doc_id: Unique identifier for the document. Either the UUID or the urlId is acceptable.
            title: The title of the document.
            text: The body of the document in markdown.
            append: If true the text field will be appended to the end
                    of the existing document, rather than the default behavior of
                    replacing it. This is potentially useful for things like logging
                    into a document.
            publish: Whether this document should be published and made visible to other team members, if a draft
            done: Whether the editing session has finished, this will
                  trigger any notifications. This property will soon be deprecated.

        Returns:
            DocumentResponse: The response object for the updated document
        """
        data = {
            "id": str(doc_id),
            "append": append,
            "publish": publish,
            "done": done
        }
        if title:
            data["title"] = title
        if text:
            data["text"] = text

        response = self.post("update", data=data)
        return DocumentResponse(**response.json())

    def search(
            self,
            query: str,
            collection_id: Optional[Union[UUID, str]] = None,
            user_id: Optional[Union[UUID, str]] = None,
            document_id: Optional[Union[UUID, str]] = None,
            status_filter: Optional[DocumentStatus] = None,
            date_filter: Optional[Period] = None,
            pagination: Optional[Union[Pagination, Dict]] = None
    ) -> DocumentSearchResultResponse:
        """
        Full-text search feature. Use of keywords is most effective.

        Args:
            query: Full-text search query
            collection_id: Optionally filter to a specific collection
            user_id: Optionally filter to a specific editor user
            document_id: You also can just put the id of the document to search within
            status_filter: Any documents that are not in the specified status will be filtered out
            date_filter: Any documents that have not been updated within the specified period will be filtered out
            pagination: Custom pagination (default: offset=0, limit=25)
        Returns:
            DocumentSearchResultResponse: Contains search results, policies, and pagination info
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
            if isinstance(pagination, Pagination):
                data.update(pagination.dict())
            elif isinstance(pagination, Dict):
                data.update(pagination)

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
            DocumentListResponse: The response object with the list of draft documents
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
            DocumentListResponse: The response object with the list of recently viewed documents
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
            DocumentAnswerResponse: The response object for the answer and related documents
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

    def templatize(self, doc_id: Union[UUID, str], publish: bool = False) -> DocumentResponse:
        """
        Create a template from a document

        Args:
            doc_id: Document ID to templatize
            publish: Whether to publish immediately

        Returns:
            DocumentResponse: The response object for the created template
        """
        data = {
            "id": str(doc_id),
            "publish": publish
        }
        response = self.post("templatize", data=data)
        return DocumentResponse(**response.json())

    def unpublish(self, doc_id: Union[UUID, str]) -> DocumentResponse:
        """
        Unpublish a document

        Args:
            doc_id: Document ID to unpublish

        Returns:
            DocumentResponse: The response object for the unpublished document
        """
        response = self.post("unpublish", data={"id": str(doc_id)})
        return DocumentResponse(**response.json())

    def move(
            self,
            doc_id: Union[UUID, str],
            collection_id: Union[UUID, str],
            parent_document_id: Optional[Union[UUID, str]] = None
    ) -> DocumentMoveResponse:
        """
        Move a document to a new location or collection.md. If no parent document
        is provided, the document will be moved to the collection.md root.

        Args:
            doc_id: Document ID to move. Either the UUID or the urlId is acceptable.
            collection_id: Target collection ID.
            parent_document_id: Target parent document ID.

        Returns:
            DocumentMoveResponse: The response object with the updated documents and collections data
        """
        data = {
            "id": str(doc_id),
            "collectionId": str(collection_id)
        }
        if parent_document_id:
            data["parentDocumentId"] = str(parent_document_id)

        response = self.post("move", data=data)
        return DocumentMoveResponse(**response.json())

    def archive(self, doc_id: Union[UUID, str]) -> DocumentResponse:
        """
        Archive a document

        Args:
            doc_id: Document ID to archive

        Returns:
            DocumentResponse: The response object for the archived document
        """
        response = self.post("archive", data={"id": str(doc_id)})
        return DocumentResponse(**response.json())

    def restore(
            self,
            doc_id: Union[UUID, str],
            revision_id: Optional[Union[UUID, str]] = None
    ) -> DocumentResponse:
        """
        Restore a document

        Args:
            doc_id: Document ID to restore
            revision_id: Optional revision ID to restore to

        Returns:
            DocumentResponse: The response object for the restored document
        """
        data = {"id": str(doc_id)}
        if revision_id:
            data["revisionId"] = str(revision_id)

        response = self.post("restore", data=data)
        return DocumentResponse(**response.json())

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
            query: Optional filter by username

        Returns:
            DocumentUsersResponse: The response object with the list of users with access
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
            query: Optional filter by username

        Returns:
            DocumentMembershipsResponse: The response object with the list of direct memberships
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
            permission: Optional[Permission] = None
    ) -> DocumentMembershipsResponse:
        """
        Add a user to a document

        Args:
            doc_id: Document ID
            user_id: User ID to add
            permission: Optional permission level

        Returns:
            DocumentMembershipsResponse: The response object with the list of updated users and memberships
        """
        data = {
            "id": str(doc_id),
            "userId": str(user_id)
        }
        if permission:
            data["permission"] = permission

        response = self.post("add_user", data=data)
        return DocumentMembershipsResponse(**response.json())

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

    

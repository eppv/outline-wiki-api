from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.comment import CommentResponse, CommentListResponse, Data


class Comments(Resources):
    """
    `Comments` represent a comment either on a selection of text in a document
    or on the document itself.

    Methods:
        create: Create a comment
        info: Retrieve a comment
        update: Update a comment
        delete: Delete a comment
        list: List all comments
    """

    _path: str = "/comments"

    def create(
        self,
        document_id: UUID | str,
        comment_id: UUID | str | None = None,
        parent_comment_id: UUID | str | None = None,
        data: dict | None = None,
        text: str | None = None,
    ):
        """
        Add a comment or reply to a document, either `data` or `text` is required.

        Args:
            document_id: The ID of the document to add the comment to
            comment_id: The optional id of the comment to add
            parent_comments_id: The optional id of the parent comment to add the comment to
            data: The body of the comment
            text: The body of the comment in markdown

        Returns:
            The created comment
        """
        payload = {"documentId": str(document_id)}
        if comment_id:
            payload["id"] = str(comment_id)
        if parent_comment_id:
            payload["parentCommentId"] = str(parent_comment_id)
        if data:
            payload["data"] = data
        if text:
            payload["text"] = text

        response = self.post("create", data=payload)
        return CommentResponse(**response.json())

    def info(self, comment_id: UUID | str) -> CommentResponse:
        """
        Retrieve a single comment by its ID.

        Args:
            comment_id: The ID of the comment to retrieve

        Returns:
            The requested comment
        """
        response = self.post("info", data={"id": str(comment_id)})
        return CommentResponse(**response.json())

    def update(
        self,
        comment_id: UUID | str,
        data: Data | None = None,
    ) -> CommentResponse:
        """
        Update an existing comment.

        Args:
            comment_id: The ID of the comment to update
            data: The updated body of the comment

        Returns:
            The updated comment
        """
        payload = {"id": str(comment_id)}
        if data:
            payload["data"] = data

        response = self.post("update", data=payload)
        return CommentResponse(**response.json())

    def delete(self, comment_id: UUID | str) -> CommentResponse:
        """
        Delete a comment by its ID.

        Args:
            comment_id: The ID of the comment to delete

        Returns:
            The deleted comment
        """
        response = self.post("delete", data={"id": str(comment_id)})
        return CommentResponse(**response.json())

    def list(
        self,
        collection_id: UUID | str | None = None,
        document_id: UUID | str | None = None,
        direction: str | None = None,
        include_anchor_text: bool | None = None,
        pagination: Pagination | None = None,
        sorting: Sort | None = None,
    ) -> CommentListResponse:
        """
        List all comments, with optional filters for collection or document.

        Args:
            collection_id: The ID of the collection to filter comments by
            document_id: The ID of the document to filter comments by
            direction: The direction of the comments to filter by (e.g., "inbound", "outbound")
            include_anchor_text: Whether to include anchor text in the response
            pagination: Pagination settings
            sorting: Sorting settings

        Returns:
            A list of comments matching the filters
        """
        data = {}
        if collection_id:
            data["collectionId"] = str(collection_id)
        if document_id:
            data["documentId"] = str(document_id)
        if direction:
            data["direction"] = direction
        if include_anchor_text is not None:
            data["includeAnchorText"] = include_anchor_text
        if pagination:
            data.update(pagination)
        if sorting:
            data.update(sorting)

        response = self.post("list", data=data)
        return CommentListResponse(**response.json())

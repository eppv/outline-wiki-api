from uuid import UUID
from .base import Resources


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
        return response.json()

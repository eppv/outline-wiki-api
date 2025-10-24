"""
Classes for Events resources group

Classes:
    Events: Events resources method group main class
"""

from uuid import UUID
from .base import Resources
from ..models.response import Pagination, Sort
from ..models.event import EventListResponse


class Events(Resources):
    """
    Events are an audit trail of important events that happen in the knowledge base.

    Methods:
        list: List all events
    """

    _path: str = "/events"

    def list(
        self,
        name: str | None = None,
        actor_id: str | UUID | None = None,
        document_id: str | UUID | None = None,
        collection_id: str | UUID | None = None,
        audit_log: bool | None = None,
        pagination: Pagination | None = None,
        sorting: Sort | None = None,
    ):
        """
        List all events

        Args:
            name: Filter to a specific event, e.g. "collections.create".
              Event names are in the format "objects.verb"
            actor_id: Filter to events performed by the selected user
            document_id: Filter to events performed in the selected document
            collection_id: Filter to events performed in the selected collection
            audit_log: Whether to return detailed events suitable for an
              audit log. Without this flag less detailed event types will
              be returned.
            pagination: Pagination parameters
            sorting: Sorting parameters

        Returns:
            List of events
        """
        data = {}
        if name:
            data["name"] = name
        if actor_id:
            data["actor_id"] = str(actor_id)
        if document_id:
            data["document_id"] = str(document_id)
        if collection_id:
            data["collection_id"] = str(collection_id)
        if audit_log:
            data["audit_log"] = audit_log
        if pagination:
            data["pagination"] = pagination
        if sorting:
            data["sorting"] = sorting
        response = self.post("list", data=data)
        return EventListResponse(**response.json())

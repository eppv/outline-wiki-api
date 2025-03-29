
from typing import Optional
from .base import Resources
from ..models.various import Document


class Documents(Resources):
    """
    `Documents` are what everything else revolves around. A document represents
    a single page of information and always returns the latest version of the
    content. Documents are stored in [Markdown](https://spec.commonmark.org/)
    formatting.
    """
    _path: str = 'documents'

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

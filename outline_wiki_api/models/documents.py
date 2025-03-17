
from typing import Optional
from dataclasses import dataclass
from outline_wiki_api.base import EntityCollection


@dataclass
class Document:

    def __init__(
            self,
            title: str = 'Untitled',
            text: str = '',
            collection_id: str = '',
            parent_document_id: str = '',
            template_id: Optional[str] = None,
            template: bool = False,
            publish: bool = True) -> None:

        self.title = title
        self.text = text
        self.collection_id = collection_id
        self.parent_document_id = parent_document_id
        self.template_id = template_id
        self.template = template
        self.publish = publish


class Documents(EntityCollection):
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
            "userId": user_id if user_id else f"{self.client.auth.user_id}",
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

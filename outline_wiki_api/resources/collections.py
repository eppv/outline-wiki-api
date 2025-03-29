
from typing import Optional
from .base import Resources


class Collections(Resources):
    """
    `Collections` represent grouping of documents in the knowledge base, they
    offer a way to structure information in a nested hierarchy and a level
    at which read and write permissions can be granted to individual users or
    groups of users.
    """
    _path: str = 'collections'

    def list(self,
             offset: int = 1,
             limit: int = 25,
             sort: str = 'updatedAt',
             direction: str = 'DESC',
             query: str = '',
             status_filter: Optional[list] = None):
        method = f'{self._path}.list'
        data = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "direction": direction,
            "query": query,
            "statusFilter": status_filter if status_filter else []
        }
        print(data)
        return self._client.request(
            method=method,
            data=data
        )
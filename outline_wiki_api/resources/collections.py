
from typing import Optional
from outline_wiki_api.resources.base import Resources


class Collections(Resources):
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
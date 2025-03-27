from outline_wiki_api.resources.base import Resources


class Auth(Resources):
    _path = 'auth'

    def __init__(self, client):
        super().__init__(client)
        self._user_id = None

    @property
    def user_id(self):
        return self._user_id

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        endpoint = f'{self._path}.config'
        return self.post(endpoint=endpoint)

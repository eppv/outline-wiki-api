from outline_wiki_api.resources.base import Resources


class Auth(Resources):
    _path = 'auth'

    def __init__(self, client):
        super().__init__(client)
        data = self.info().json()['data']
        self._user_id = data['user']['id']

    @property
    def user_id(self):
        return self._user_id

    def config(self):
        """
        Retrieve authentication options
        :return:
        """
        method = f'{self._path}.config'
        return self.client.post(method=method)

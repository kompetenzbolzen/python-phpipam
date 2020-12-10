from .backend import phpipamBackend
from .resources import phpipamResource

class phpipam:
    """
    phpIPAM API Implementation
    ReadOnly because I don't need the writing bit

    https://phpipam.net/api-documentation/
    """

    def __init__(self, api_url, app_id, api_user, api_password):
        self._backend = phpipamBackend(api_url, app_id, api_user, api_password)

    def __getattr__(self, item):
        return phpipamResource(self._backend, item)

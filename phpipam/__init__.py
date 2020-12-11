from .backend import phpipamBackend
from .resources import phpipamResource

class phpipam:
    """
    phpIPAM API Implementation

    Attributes
    ----------
    sections
    subnets
    addresses
    devices

    https://phpipam.net/api-documentation/
    """

    def __init__(self, api_url, app_id, api_user, api_password):
        """
        Parameters
        ----------
        api_url : str
            URL of phpIPAM instance. Example: https://phpipam.example.com/
        app_id : str
            AppID configrued in API settings
        api_user : str
            username, leave empty to use static token authentification
        api_password : str
            password or static authentification token
        """

        self._backend = phpipamBackend(api_url, app_id, api_user, api_password)

    def __getattr__(self, item):
        return phpipamResource(self._backend, item)

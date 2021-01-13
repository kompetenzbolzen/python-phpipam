#
# phpipam/__init__.py
# (c) 2021 Jonas Gunz <himself@jonasgunz.de>
# License: MIT
#
from .backend import PhpipamBackend
from .resources import PhpipamResource

class PhpipamAPI:
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

        self._backend = PhpipamBackend(api_url, app_id, api_user, api_password)

    def __getattr__(self, item):
        return PhpipamResource(self._backend, item)

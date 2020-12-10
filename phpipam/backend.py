import requests
import json
import datetime
from dateutil.parser import parse as datetime_parse

class apiConnectionException(Exception):
    pass

class apiQueryException(Exception):
    pass

class apiObjectNotFoundException(Exception):
    pass

class phpipamBackend:
    def __init__(self, api_url, app_id, api_user, api_password):
        """
        Parameters
        ----------
        api_url : str
            URL of the phpIPAM instance. Example: https://phpipam.example.com/
        app_id : str
            AppID set in phpIPAM API settings
        api_user : str
            username, leave blank to use static token-authentication
        api_password : str
            user password or static auth token

        Raises
        ------
        apiConnectionException
            if the connection/authentification fails
        """

        self.api_url = api_url.strip('/') + '/api/' + app_id
        self.api_user = api_user
        self.api_password = api_password

        # Check for static auth
        if len(self.api_user) == 0:
            self.api_token = self.api_password
            self.api_token_expires = ""
        else:
            self._getApiToken()

    def _getApiToken(self):
        data = requests.post(self.api_url + "/user", auth=(self.api_user,self.api_password)).json()
        if not data['success']:
            raise apiConnectionException('Failed to authenticate: ' + str(data['code']))

        self.api_token = data['data']['token']
        self.api_token_expires = data['data']['expires']


    def _isTokenExpired(self):
        # static auth does not expire
        if len(self.api_token_expires) == 0:
            return False

        expiration = datetime_parse(self.api_token_expires)

        return expiration < datetime.datetime.now()

    def request ( self, method, url, data = {} ):
        """Wrapper for _req for checking result and only returning data"""

        if self._isTokenExpired():
            self._getApiToken()

        data = requests.request(method, self.api_url + url, data=data, headers={'token':self.api_token}).json()

        if not 'success' in data or not data['success']:
            raise apiQueryException("Query failed with code " + str(data['code']) + ": " + str(data['message']))

        return data['data']


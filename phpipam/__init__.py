
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

class phpipam:
    """
    phpIPAM API Implementation
    ReadOnly because I don't need the writing bit

    https://phpipam.net/api-documentation/
    """

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

    def _req( self, method, url, data = {} ):
        if self._isTokenExpired():
            self._getApiToken()

        return requests.request(method, self.api_url + url, data=data, headers={'token':self.api_token}).json()

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

    # TODO remove
    def _checkTokenExpired(self):
        data = self._req('GET', '/user/')
        return data['success']

    def _checkReq ( self, method, url, data = {} ):
        """Wrapper for _req for checking result and only returning data"""

        data = self._req( method, url, data )

        if not 'success' in data or not data['success']:
            raise apiQueryException("Query failed with code " + str(data['code'] + ": " + str(['message'])))

        return data['data']

    #
    def getSections(self):
        """
        Get the complete list of dictionaries describing sections
        Returns: list of dicts
        """

        return self._checkReq('GET', '/sections/')

    def getSectionById(self, section_id):
        """
        Get a section by id

        Parameters
        ----------
        section_id : str

        Returns: dict
        """

        return self._checkReq('GET', f'/sections/{section_id}')


    def getSectionByName(self, name):
        """
        Find a section by name

        Parameters
        ----------
        name : str
            name of the section to search for

        Returns: dict

        Raises
        ------
        apiObjectNotFoundException
            if no section matches name
        """

        data = self.getSections()

        for section in data:
            if 'name' in section and section['name'] == name:
                return section

        raise apiObjectNotFoundException(f"Section {name} was not found.")

    def getSubnets(self, section_id):
        """
        Get the complete list of dictionaries describing subnets of a section

        Parameters
        ----------
        section_id : str
        """

        return self._checkReq('GET', f'/sections/{section_id}/subnets')

    def getSubnetById(self, subnet_id):
        """
        Get a section by id

        Parameters
        ----------
        subnet_id : str
        """

        return self._checkReq('GET', f'/subnets/{subnet_id}')


#
# phpipam/backend.py
# (c) 2021 Jonas Gunz <himself@jonasgunz.de>
# License: MIT
#
import requests
import json
import datetime
from dateutil.parser import parse as datetime_parse

class ApiConnectionException(Exception):
    pass

class ApiQueryException(Exception):
    pass

class ApiObjectNotFoundException(Exception):
    pass

class PhpipamBackend:
    def __init__(self, api_url, app_id, api_user, api_password):
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
            raise ApiConnectionException('Failed to authenticate: ' + str(data['code']) + ' ' + data['message'])

        self.api_token = data['data']['token']
        self.api_token_expires = data['data']['expires']


    def _isTokenExpired(self):
        # static auth does not expire
        if len(self.api_token_expires) == 0:
            return False

        expiration = datetime_parse(self.api_token_expires)

        return expiration < datetime.datetime.now()

    def request ( self, method, url, data = {} ):
        if self._isTokenExpired():
            self._getApiToken()

        data = requests.request(method, self.api_url + url, data=data, headers={'token':self.api_token}).json()

        if not 'success' in data or not data['success']:
            raise ApiQueryException("Query failed with code " + str(data['code']) + ": " + str(data['message']))

        return data['data']


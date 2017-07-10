#!/usr/bin/env python
from zeep import Client as Zeep
from zeep import xsd

class UltiProClient:

    def __init__(self, username, password, client_access_key, user_access_key, base_url):
        assert(username is not None)
        assert(password is not None)
        assert(client_access_key is not None)
        assert(user_access_key is not None)
        assert (base_url is not None)
        self.username = username
        self.password = password
        self.client_access_key = client_access_key
        self.user_access_key = user_access_key
        self.base_url = base_url

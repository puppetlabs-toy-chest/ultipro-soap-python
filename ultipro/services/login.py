from zeep import Client as Zeep
from zeep import xsd
from ultipro.helpers import backoff_hdlr
import requests
import backoff # Helps handle intermittent 405 errors from server
import logging

endpoint = 'LoginService'

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def authenticate(client):
    login_header = {
        'UserName': client.username,
        'Password': client.password,
        'ClientAccessKey': client.client_access_key,
        'UserAccessKey': client.user_access_key,
    }

    # Log in and get session token
    zeep_client = Zeep(f"{client.base_url}{endpoint}")
    result = zeep_client.service.Authenticate(_soapheaders=login_header)
    client.token = result['Token']

    # Create xsd ComplexType header - http://docs.python-zeep.org/en/master/headers.html
    header = xsd.ComplexType([
        xsd.Element(
            '{http://www.ultimatesoftware.com/foundation/authentication/ultiprotoken}UltiProToken',
            xsd.String()),
        xsd.Element(
            '{http://www.ultimatesoftware.com/foundation/authentication/clientaccesskey}ClientAccessKey',
            xsd.String()),
    ])

    # Add authenticated header to client object
    client.session_header = header(UltiProToken=client.token, ClientAccessKey=client.client_access_key)


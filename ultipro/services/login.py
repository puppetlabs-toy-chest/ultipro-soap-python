from zeep import Client as Zeep
from zeep import xsd

endpoint = '/LoginService?wsdl'

def authenticate(client):
    login_header = {
        'UserName': client.username,
        'Password': client.password,
        'ClientAccessKey': client.client_access_key,
        'UserAccessKey': client.user_access_key,
    }

    # Log in and get session token
    zeep_client = Zeep("{0}{1}".format(client.base_url, endpoint))
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

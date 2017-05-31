from zeep import Client as Zeep
from zeep import xsd

endpoint = '/BiDataService?wsdl'

def log_on_with_token(client):
    credentials = {
        'Token': client.token,
        'ClientAccessKey': client.client_access_key
    }

    # Log on to get DataContext object with auth
    zeep_client = Zeep(client.base_url + endpoint)
    element = zeep_client.get_element('ns5:LogOnWithTokenRequest')
    obj = element(**credentials)

    return zeep_client.service.LogOnWithToken(obj)

def get_report_list(client, context):
    zeep_client = Zeep(client.base_url + endpoint)
    return zeep_client.service.GetReportList(context)

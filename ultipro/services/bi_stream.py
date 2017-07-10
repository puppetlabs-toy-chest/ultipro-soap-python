from zeep import Client as ZeepClient
from zeep import Plugin

endpoint = 'BiStreamingService?wsdl'

def retrieve_report(client, report_key):
    zeep_client = ZeepClient(client.base_url + endpoint)
    return zeep_client.service.RetrieveReport(_soapheaders={'ReportKey': report_key})

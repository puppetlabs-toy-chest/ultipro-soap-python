from zeep import Client as ZeepClient
from zeep import Plugin
from zeep import xsd
from lxml import etree
from requests import Session
from zeep.transports import Transport

endpoint = 'BiDataService?wsdl'

def log_on_with_token(client):
    credentials = {
        'Token': client.token,
        'ClientAccessKey': client.client_access_key
    }

    # Log on to get ns5:DataContext object with auth
    zeep_client = ZeepClient("{0}{1}".format(client.base_url, endpoint))
    element = zeep_client.get_element('ns5:LogOnWithTokenRequest')
    obj = element(**credentials)

    return zeep_client.service.LogOnWithToken(obj)

def get_report_list(client, context):
    zeep_client = ZeepClient("{0}{1}".format(client.base_url, endpoint))
    return zeep_client.service.GetReportList(context)

def get_report_parameters(client, report_path, context):
    zeep_client = ZeepClient("{0}{1}".format(client.base_url, endpoint))
    return zeep_client.service.GetReportParameters(report_path, context)

def execute_report(client, context, report_path, delimiter=','):
    session = Session()
    session.headers.update({'US-DELIMITER': delimiter})
    transport = Transport(session=session)

    payload = {'ReportPath': report_path}
    zeep_client = ZeepClient("{0}{1}".format(client.base_url, endpoint), transport=transport)
    element = zeep_client.get_element('ns5:ReportRequest')
    obj = element(**payload)
    r = zeep_client.service.ExecuteReport(request=obj, context=context)
    return r['ReportKey']


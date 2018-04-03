from zeep import Client as ZeepClient
from zeep import Plugin
from zeep import xsd
from zeep.transports import Transport
from lxml import etree
from ultipro.helpers import backoff_hdlr
import requests
import backoff # Helps handle intermittent 405 errors from server

endpoint = 'BiDataService'

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def log_on_with_token(client):
    # print(inspect.getmembers(client))
    credentials = {
        'Token': client.token,
        'ClientAccessKey': client.client_access_key
    }

    # Log on to get ns5:DataContext object with auth
    zeep_client = ZeepClient(f"{client.base_url}{endpoint}")
    element = zeep_client.get_element('ns5:LogOnWithTokenRequest')
    obj = element(**credentials)
    # print(inspect.getmembers(obj))
    return zeep_client.service.LogOnWithToken(obj)

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def get_report_list(client, context):
    zeep_client = ZeepClient(f"{client.base_url}{endpoint}")
    return zeep_client.service.GetReportList(context)

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def get_report_parameters(client, report_path, context):
    zeep_client = ZeepClient(f"{client.base_url}{endpoint}")
    return zeep_client.service.GetReportParameters(report_path, context)

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def execute_report(client, context, report_path, delimiter=','):
    session = requests.Session()
    session.headers.update({'US-DELIMITER': delimiter})
    transport = Transport(session=session)
    payload = {'ReportPath': report_path}
    zeep_client = ZeepClient(f"{client.base_url}{endpoint}",
                             transport=transport)
    element = zeep_client.get_element('ns5:ReportRequest')
    obj = element(**payload)
    r = zeep_client.service.ExecuteReport(request=obj, context=context)
    return r['ReportKey']


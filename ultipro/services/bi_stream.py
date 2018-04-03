from zeep import Client as ZeepClient
from zeep import Plugin
import ultipro.helpers
from ultipro.helpers import backoff_hdlr
import requests
import backoff # Helps handle intermittent 405 errors from server

endpoint = 'BiStreamingService'

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=8, on_backoff=backoff_hdlr)
def retrieve_report(client, report_key):
    zeep_client = ZeepClient(f"{client.base_url}{endpoint}")
    return zeep_client.service.RetrieveReport(_soapheaders={'ReportKey': report_key})

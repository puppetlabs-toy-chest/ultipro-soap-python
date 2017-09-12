from zeep import Client as ZeepClient
from ultipro.services import bi_data, bi_stream

def execute_and_fetch(client, report_path, delimiter=','):
    context = bi_data.log_on_with_token(client)
    k = bi_data.execute_report(client, context, report_path, delimiter=delimiter)
    r = bi_stream.retrieve_report(client, k)
    return r['body']['ReportStream'].decode('unicode-escape')


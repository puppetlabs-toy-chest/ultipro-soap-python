import zeep
import logging
import pandas as pd
import io
# from lxml import etree
# from zeep import Plugin

# class LoggingPlugin(Plugin):

#     def ingress(self, envelope, http_headers, operation):
#         print(etree.tostring(envelope, pretty_print=True))
#         return envelope, http_headers

#     def egress(self, envelope, http_headers, operation, binding_options):
#         print(etree.tostring(envelope, pretty_print=True))
#         return envelope, http_headers

def serialize(response):
    return zeep.helpers.serialize_object(response)

def write_file(report_stream, path):
	f = open(path, "w")
	f.write(report_stream)
	f.close()

def to_dataframe(report_stream, delimiter):
    p = pd.read_csv(io.StringIO(report_stream), delimiter=delimiter, encoding='utf-8', index_col=False)
    p.index.name = 'index'
    return p



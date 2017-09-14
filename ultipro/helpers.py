import configparser
import zeep
import logging
import pandas as pd
from pandas_gbq import gbq
import io
from lxml import etree
from zeep import Plugin

# Use this plugin as a kwarg for the zeep class to print SOAP messages
class LoggingPlugin(Plugin):

    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

def backoff_hdlr(details):
    """ Prints backoff debug messages"""
    print("Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target}".format(**details))

def backoff_hdlr_with_args(details):
    """ USE FOR DEBUGGING ONLY - Prints out all details about backoff events,
    including ultipro client object with credentials, to STDOUT
    """
    print("Backing off {wait:0.1f} seconds after {tries} tries "
          "calling function {target} with args {args} and kwargs "
          "{kwargs}".format(**details))

def read_conf(conf):
    parser = configparser.ConfigParser()
    parser.read(conf)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv[f"{section}.{key}"] = value
    return rv

def serialize(response):
    return zeep.helpers.serialize_object(response)

def write_file(report_stream, path):
    """Writes a stream to a file"""
    f = open(path, "w")
    f.write(report_stream)
    f.close()

def csv_stream_to_dataframe(report_stream, delimiter):
    """Reads a streaming csv into a pandas DataFrame."""
    report = io.StringIO(report_stream)
    df = pd.read_csv(report, sep=delimiter, encoding='utf-8', index_col=False)
    return df

def dataframe_to_bigquery(df):
    """Writes a DataFrame to Big Query. Column names will be downcased and
    all non-alphanumeric characters converted to underscores."""
    df.columns = df.columns.str.strip().str.lower().str.replace(r'[^\w]', '_')

    # gbq.to_gbq(
    #   dataframe=df,
    #   destination_table='lake1.pond1',
    #   project_id='pubsub-bq-pipe-1',
    #   chunksize=10000,
    #   verbose=True,
    #   reauth=False,
    #   if_exists='append',
    #   private_key="./pubsub-bq-pipe-1-a865bbaa5f48.json",
    #   auth_local_webserver=False)

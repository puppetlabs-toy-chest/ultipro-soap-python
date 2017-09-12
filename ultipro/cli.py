import click
import os
import time
import datetime
import decimal
import json
import csv
import configparser
from ultipro.client import UltiProClient
import ultipro.helpers as helpers
from ultipro.services import *

timestr = time.strftime("%Y%m%d-%H%M%S")
HOME = os.path.expanduser('~')
DEFAULT_BASENAME = f"UltiPro-Report-{timestr}.csv"
DEFAULT_CONFFILE = os.path.join(click.get_app_dir('ultipro-soap-python'), 'config.ini')
DEFAULT_OUTFILE = f"{HOME}/Desktop/{DEFAULT_BASENAME}"

class UltiProEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.UltiProEncoder.default(self, obj)

@click.group()
@click.option('--conffile', '-f', default=DEFAULT_CONFFILE, help='UltiPro API config.ini file path.', type=click.Path(exists=True))
@click.option('--outfile', '-o', default=DEFAULT_OUTFILE, help='File to write to, with extension. (default = .csv).', type=click.Path())
@click.option('--print/--no-print', default=False, help='Whether to print results to the console.')
@click.pass_context
def cli(ctx, conffile, outfile, print):
    click.echo(f"Using config file: {conffile}")
    ctx.obj = read_conf(conffile)
    ctx.obj['outfile'] = outfile
    ctx.obj['print'] = print

@cli.command()
@click.argument('report_path')
@click.pass_context
def get_report(ctx, report_path):
    client = create_client(ctx)
    login.authenticate(client)
    data = bi_reports.execute_and_fetch(client, report_path)
    if ctx.obj['print']:
        print(data)
    if ctx.obj['outfile']:
        helpers.write_file(data, ctx.obj['outfile'])
        click.echo(f"Saved output file as: {ctx.obj['outfile']}")
    return data

def read_conf(conf):
    parser = configparser.ConfigParser()
    parser.read(conf)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv[f"{section}.{key}"] = value
    return rv

def write_json(ctx, r):
    outfile = ctx.obj['outfile'] + '.json'
    click.echo(f"JSON saved to: {outfile}")
    json_str = json.dumps(r, cls=UltiProEncoder, ensure_ascii=False, indent=4, sort_keys=True)
    with open(outfile, 'w') as f:
        f.write(json_str)
    return json_str

def create_client(ctx):
    client = UltiProClient(
        ctx.obj['ULTIPRO.username'],
        ctx.obj['ULTIPRO.password'],
        ctx.obj['ULTIPRO.client_access_key'],
        ctx.obj['ULTIPRO.user_access_key'],
        ctx.obj['ULTIPRO.base_url']
    )
    return client
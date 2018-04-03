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
DEFAULT_CONFIG = os.path.join(click.get_app_dir('ultipro-soap-python'), 'config.ini')
DEFAULT_OUTFILE = f"{HOME}/Desktop/{DEFAULT_BASENAME}"

class UltiProEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.UltiProEncoder.default(self, obj)

@click.group()
@click.option('--config',
              '-f',
              default=DEFAULT_CONFIG,
              help='UltiPro API config.ini file path.',
              type=click.Path(exists=True))
@click.option('--outfile',
              '-o',
              default=DEFAULT_OUTFILE,
              help='File to write to, with extension.',
              type=click.Path())
@click.option('--print/--no-print',
              default=False,
              help='Whether to print results to the console.')
@click.pass_context
def cli(ctx, config, outfile, print):
    click.echo(f"Using config file: {config}")
    ctx.obj = helpers.read_conf(config)
    ctx.obj['outfile'] = outfile
    ctx.obj['print'] = print

## This is the CLI code for querying via SOAP
## Currently removed in favor of pulling reports via BI endpoint only
## Could be refactored and reimplemented without difficulty if atomic
## interaction with UP is needed.

## This find command needs to be reimplemented to accept either an
## employee identifier or search string(s), then do find or
## get by ID accordingly

# @cli.command()
# @click.option('--search-type', type=click.Choice['find', 'eid'],
#                help='Whether to use search strings in the find operation or '
#                'search by employee identifier')
# @click.option('--firstname',
#               '-f',
#               help='Employee Property: FirstName')
# @click.option('--lastname',
#               '-l',
#               help='Employee Property: LastName')
# @click.option('--employee_number',
#               '-n',
#               help='Employee Property: EmployeeNumber')
# @click.option('--email',
#               '-e',
#               help='Employee Property: EmployeeNumber')
# @click.option('--jobs',
#               default=False,
#               help='API Operation: FindJobs',
#               type=click.BOOL)
# @click.option('--people',
#               default=False,
#               help='API Operation: FindPeople',
#               type=click.BOOL)
# @click.option('--addresses',
#               default=False,
#               help='API Operation: FindAddresses',
#               type=click.BOOL)
# @click.option('--terms',
#               default=False,
#               help='API Operation: FindTerminations',
#               type=click.BOOL)
# @click.option('--phones',
#               default=False,
#               help='API Operation: FindPhoneInformations',
#               type=click.BOOL)
# @click.option('--employees',
#               default=False,
#               help='API Operation: FindEmploymentInformations',
#               type=click.BOOL)
# @click.option('--comps',
#               default=False,
#               help='API Operation: Find Compensation',
#               type=click.BOOL)
# @click.pass_context
# def get(ctx, by_id, firstname, lastname, employee_number, email, jobs, people,
#          addresses, terms, phones, employees, comps):

#     client = create_client(ctx)
#     login.authenticate(client)

#     query = {}
#     if first:
#         query['FirstName'] = first
#     if last:
#         query['LastName'] = last
#     if eid:
#         query['EmployeeNumber'] = eid
#     if email:
#         query['Email'] = email

#     if by_id = False

#     responses = []
#     if jobs:
#         print(ultipro.helpers.serialize(employee_job.find_jobs(client, query)))
#     if people:
#         responses.append(ultipro.helpers.serialize(services.employee_person.find_people(client, query)))
#     if addresses:
#         responses.append(ultipro.helpers.serialize(c.find_addresses(query)))
#     if terms:
#         responses.append(ultipro.helpers.serialize(c.find_terminations(query)))
#     if phoneinfo:
#         responses.append(ultipro.helpers.serialize(c.find_phone_informations(query)))
#     if employinfo:
#         responses.append(ultipro.helpers.serialize(c.find_employment_informations(query)))

#     if eidcompile:
#         r = ultipro.helpers.compile_on_eid(responses)
#     else:
#         r = responses

#     if ctx.obj['format'] == 'concur_csv':
#         pass

#     if ctx.obj['format'] == 'json':
#         r = write_json(ctx, r)

#     if ctx.obj['printout']:
#         click.echo(r)

# @click.pass_context
# def get_by_id(ctx, firstname, lastname, employeenumber, job_info, person_info,
#               address_info, term_info, phone_info, employee_info, comp_info):

@cli.command()
@click.argument('report_path')
@click.pass_context
def report(ctx, report_path):
    client = create_client(ctx)
    login.authenticate(client)
    data = bi_reports.execute_and_fetch(client, report_path)
    if ctx.obj['print']:
        print(data)
    if ctx.obj['outfile']:
        helpers.write_file(data, ctx.obj['outfile'])
        click.echo(f"Saved output file as: {ctx.obj['outfile']}")
    return data

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
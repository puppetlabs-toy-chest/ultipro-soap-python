import click
import os
import time
import datetime
import decimal
import json
import csv
import configparser
import ultipro.client
import ultipro.helpers
from ultipro.services import *

timestr = time.strftime("%Y%m%d-%H%M%S")
HOME = os.path.expanduser('~')
DEFAULT_BASENAME = "/UltiPro_Report-{0}".format(timestr)
DEFAULT_CONFFILE = os.path.join(click.get_app_dir('ultipro-soap-python'), 'config.ini')
DEFAULT_OUTFILE = "{0}/Desktop{1}".format(HOME, DEFAULT_BASENAME)

class UltiProEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.UltiProEncoder.default(self, obj)

@click.group()
@click.option('--conffile', '-f', default=DEFAULT_CONFFILE, help='UltiPro API config.ini file path.', type=click.Path(exists=True))
@click.option('--outfile', '-o', default=DEFAULT_OUTFILE, help='File to write to, without file extension.', type=click.Path())
@click.option('--format', type=click.Choice(['json', 'concur_csv']))
@click.option('--printout/--no-printout', default=False, help='Whether to print results to the console.')
@click.pass_context
def cli(ctx, conffile, outfile, format, printout):
    click.echo('Using config file: %s' % conffile)
    ctx.obj = read_conf(conffile)
    ctx.obj['outfile'] = outfile
    ctx.obj['format'] = format
    ctx.obj['printout'] = printout

@cli.command()
@click.option('--firstname', '-fname', help='Employee Property: FirstName')
@click.option('--lastname', '-lname', help='Employee Property: LastName')
@click.option('--employeenumber', '-eid', help='Employee Property: EmployeeNumber')
@click.option('--jobs/--no-jobs', default=False, help='API Operation: FindJobs')
@click.option('--people/--no-people', default=False, help='API Operation: FindPeople')
@click.option('--addresses/--no-addresses', default=False, help='API Operation: FindAddresses')
@click.option('--terms/--no-terms', default=False, help='API Operation: FindTerminations')
@click.option('--phoneinfo/--no-phoneinfo', default=False, help='API Operation: FindPhoneInformations')
@click.option('--employinfo/--no-employinfo', default=False, help='API Operation: FindEmploymentInformations')
@click.option('--eidcompile/--no-eidcompile', default=False, help='Whether to compile results based on eid')
@click.pass_context
def find(
    ctx,
    firstname,
    lastname,
    employeenumber,
    jobs,
    people,
    addresses,
    terms,
    phoneinfo,
    employinfo,
    eidcompile):

    client = ultipro.client.UltiProClient(
        ctx.obj['ULTIPRO.username'],
        ctx.obj['ULTIPRO.password'],
        ctx.obj['ULTIPRO.client_access_key'],
        ctx.obj['ULTIPRO.user_access_key'],
        ctx.obj['ULTIPRO.base_url']
    )

    login.authenticate(client)

    query = {}
    if firstname:
        query['FirstName'] = firstname
    if lastname:
        query['LastName'] = lastname
    if employeenumber:
        query['EmployeeNumber'] = employeenumber

    responses = []
    if jobs:
        print(ultipro.helpers.serialize(employee_job.find_jobs(client, query)))
    if people:
        responses.append(ultipro.helpers.serialize(services.employee_person.find_people(client, query)))
    if addresses:
        responses.append(ultipro.helpers.serialize(c.find_addresses(query)))
    if terms:
        responses.append(ultipro.helpers.serialize(c.find_terminations(query)))
    if phoneinfo:
        responses.append(ultipro.helpers.serialize(c.find_phone_informations(query)))
    if employinfo:
        responses.append(ultipro.helpers.serialize(c.find_employment_informations(query)))

    if eidcompile:
        r = ultipro.helpers.compile_on_eid(responses)
    else:
        r = responses

    if ctx.obj['format'] == 'concur_csv':
        pass

    if ctx.obj['format'] == 'json':
        r = write_json(ctx, r)

    if ctx.obj['printout']:
        click.echo(r)

def read_conf(conf):
    parser = configparser.ConfigParser()
    parser.read(conf)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv

def write_json(ctx, r):
    outfile = ctx.obj['outfile'] + '.json'
    click.echo("JSON saved to: %s" % outfile)
    json_str = json.dumps(r, cls=UltiProEncoder, ensure_ascii=False, indent=4, sort_keys=True)
    with open(outfile, 'w') as f:
        f.write(json_str)
    return json_str

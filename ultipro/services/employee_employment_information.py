from zeep import Client as Zeep
from zeep import xsd

endpoint = '/EmployeeEmploymentInformation?wsdl'

def find_employment_informations(client, query):
    zeep_client = Zeep(f"{client.base_url}{endpoint}")
    response = zeep_client.service.FindEmploymentInformations(
        _soapheaders=[client.session_header],
        query=query)

    return response['Results']

def get_employment_information_by_employee_identifier(client, employee_identifier):
    zeep_client = Zeep(f"{client.base_url}{endpoint}")
    if 'EmployeeNumber' in employee_identifier:
        element = zeep_client.get_element('ns6:EmployeeNumberIdentifier')
        obj = element(**employee_identifier)
    elif 'EmailAddress' in employee_identifier:
        element = zeep_client.get_element('ns6:EmailAddressIdentifier')
        obj = element(**employee_identifier)

    response = zeep_client.service.GetEmploymentInformationByEmployeeIdentifier(
        _soapheaders=[client.session_header],
        employeeIdentifier=obj)

    return response['Results']

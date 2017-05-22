#!/usr/bin/env python

from zeep import Client as Zeep
from zeep import xsd

class Client:

    def __init__(self, username, password, client_access_key, user_access_key, base_url):
        assert(username is not None)
        assert(password is not None)
        assert(client_access_key is not None)
        assert(user_access_key is not None)
        assert (base_url is not None)
        self.username = username
        self.password = password
        self.client_access_key = client_access_key
        self.user_access_key = user_access_key
        self.base_url = base_url

    def authenticate(self):
        login_header = {
            'UserName': self.username,
            'Password': self.password,
            'ClientAccessKey': self.client_access_key,
            'UserAccessKey': self.user_access_key,
        }

        # Authenticate and get session token
        client = Zeep(self.base_url + '/LoginService?wsdl')
        result = client.service.Authenticate(_soapheaders=login_header)
        self.token = result['Token']

        # Create xsd ComplexType header - http://docs.python-zeep.org/en/master/headers.html
        header = xsd.ComplexType([
            xsd.Element(
                '{http://www.ultimatesoftware.com/foundation/authentication/ultiprotoken}UltiProToken',
                xsd.String()),
            xsd.Element(
                '{http://www.ultimatesoftware.com/foundation/authentication/clientaccesskey}ClientAccessKey',
                xsd.String()),
        ])

        self.session_header = header(UltiProToken=self.token, ClientAccessKey=self.client_access_key)

    def find_jobs(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeeJob?wsdl')
        response = client.service.FindJobs(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeeJob']

    def get_job_by_employee_identifier(self, employee_identifier):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeeJob?wsdl')
        # obj1 = client.get_element('ns5:GetJobByEmployeeIdentifier')
        # ^^ Was this secret sauce?
        company_code = None
        if 'CompanyCode' in employee_identifier:
            company_code = employee_identifier['CompanyCode']
        if 'EmployeeNumber' in employee_identifier:
            elem = client.get_element('ns6:EmployeeNumberIdentifier')
            obj = elem(
                CompanyCode=company_code,
                EmployeeNumber=employee_identifier['EmployeeNumber']
            )
        elif 'EmailAddress' in employee_identifier:
            elem = client.get_element('ns6:EmailAddressIdentifier')
            obj = elem(
                CompanyCode=company_code,
                EmailAddress=employee_identifier['EmailAddress']
            )

        response = client.service.GetJobByEmployeeIdentifier(_soapheaders=[self.session_header], employeeIdentifier=obj)
        print(response)
        return response

    def find_people(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeePerson?wsdl')
        response = client.service.FindPeople(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeePerson']

    def find_addresses(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeeAddress?wsdl')
        response = client.service.FindAddresses(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeeAddress']

    def find_terminations(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeeTermination?wsdl')
        response = client.service.FindTerminations(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeeTerminationInfo']

    def find_phone_informations(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeePhoneInformation?wsdl')
        response = client.service.FindPhoneInformations(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeePhoneInformation']

    def find_employment_informations(self, query):
        self.authenticate()
        client = Zeep(self.base_url + '/EmployeeEmploymentInformation?wsdl')
        response = client.service.FindEmploymentInformations(_soapheaders=[self.session_header], query=query)
        return response['Results']['EmployeeEmploymentInformation']

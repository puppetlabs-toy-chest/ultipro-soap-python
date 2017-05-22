import zeep
import logging

def serialize(response):
    return zeep.helpers.serialize_object(response)

def compile_on_eid(responses):
    # Iterate through all response types and compile data based on EID
    compiled = {}
    for response in responses:
        for item in response:
            eid = item['EmployeeNumber']
            if eid not in compiled:
                compiled[eid] = {}
            if 'CompanyCode' not in compiled[eid]:
                compiled[eid]['CompanyCode'] = item['CompanyCode']
            if 'EmployeeNumber' not in compiled[eid]:
                compiled[eid]['EmployeeNumber'] = item['EmployeeNumber']
            if 'FirstName' not in compiled[eid]:
                compiled[eid]['FirstName'] = item['FirstName']
            if 'LastName' not in compiled[eid]:
                compiled[eid]['LastName'] = item['LastName']

            # Add additional data as sub-dicts if available
            if 'Jobs' in item:
                if 'Jobs' not in compiled[eid]:
                    compiled[eid]['Jobs'] = item['Jobs']
                elif 'Jobs' in compiled[eid]:
                    logging.warning('Multiple results for Jobs for EID: %s' % compiled[eid]['EmployeeNumber'])
            if 'Addresses' in item:
                if 'Addresses' not in compiled[eid]:
                    compiled[eid]['Addresses'] = item['Addresses']
                elif 'Addresses' in compiled[eid]:
                    logging.warning('Multiple results for Addresses for EID: %s' % compiled[eid]['EmployeeNumber'])
            if 'People' in item:
                if 'People' not in compiled[eid]:
                    compiled[eid]['People'] = item['People']
                elif 'People' in compiled[eid]:
                    logging.warning('Multiple results for People for EID: %s' % compiled[eid]['EmployeeNumber'])
            if 'TerminationInfo' in item:
                if 'TerminationInfo' not in compiled[eid]:
                    compiled[eid]['TerminationInfo'] = item['TerminationInfo']
                elif 'TerminationInfo' in compiled[eid]:
                    logging.warning('Multiple results for TerminationInfo for EID: %s' % compiled[eid]['EmployeeNumber'])
            if 'PhoneInformations' in item:
                if 'PhoneInformations' not in compiled[eid]:
                    compiled[eid]['PhoneInformations'] = item['PhoneInformations']
                elif 'PhoneInformations' in compiled[eid]:
                    logging.warning('Multiple results for PhoneInformations for EID: %s' % compiled[eid]['EmployeeNumber'])
            if 'EmploymentInformations' in item:
                if 'EmploymentInformations' not in compiled[eid]:
                    compiled[eid]['EmploymentInformations'] = item['EmploymentInformations']
                elif 'EmploymentInformations' in compiled[eid]:
                    logging.warning('Multiple results for EmploymentInformations for EID: %s' % compiled[eid]['EmployeeNumber'])

    return compiled


## Here's a sample script to help you get started:

```
# mytestfile.py
# /usr/bin/python
#
from ultiprosoap.client import UltiProSOAP
from ultiprosoap.helpers import *
import json
import datetime
import decimal
import io

# username - unique to service user
# password - unique to service user
# client_access_key - unique to organization
# user_access_key - unique to service user
# base_url - unique to organization(s)

username = <service_user_username>
password = <service_user_password>
client_access_key = <CLIENT_ACCESS_KEY>
user_access_key = <USER_ACCESS_KEY>
base_url = <https://example.ultipro.com/services>

# JSON encoder that converts datetime and decimal objects to strings
class UPJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.UPJSONEncoder.default(self, obj)

# Instantiate the UltiProSOAP class with required parameters
client = UltiProSOAP(
    username,
    password,
    client_access_key,
    user_access_key,
    base_url
    )

# Create your query according to UltiPro Getting Started docs
query = {'LastName': 'LIKE("Bryx%")'}

# Make your queries and add each response to a list of results
results = []
results.append(serialize(client.find_phone_informations(query)))
results.append(serialize(client.find_terminations(query)))
results.append(serialize(client.find_jobs(query)))
results.append(serialize(client.find_addresses(query)))
results.append(serialize(client.find_people(query)))
results.append(serialize(client.find_employment_informations(query)))

data = compile_on_eid(results)

# Process serialized data to ensure datetime and decimal types are proper strings
json = json.dumps(data, cls=UPJSONEncoder, ensure_ascii=False, indent=4, sort_keys=True)

# Write utf-8 encoded data to file
with io.open('mydata.json', 'w') as file:
    file.write(json)
```

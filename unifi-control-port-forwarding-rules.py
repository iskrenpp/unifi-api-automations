import requests
import json
import argparse
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

# Set up command-line arguments
parser = argparse.ArgumentParser(description='Change enable flag of a port forwarding rule using UniFi Dream Machine Pro API.')
parser.add_argument('--rule_name', required=True, help='Name of the port forwarding rule')
parser.add_argument('--new_enable_value', required=True, type=str, help='New enable flag value (True or False)')

args = parser.parse_args()

# Replace these values with your own
controller_url = 'https://localhost:443'
username = '<admin-user>'
password = '<admin-pass>'
site = 'default'  # The site ID, 'default' for most installations
rule_name = args.rule_name
new_enable_value = args.new_enable_value.lower() == 'true'

# Log in to the UniFi Controller
login_url = f'{controller_url}/api/auth/login'
login_data = {
    'username': username,
    'password': password
}

session = requests.Session()
response = session.post(login_url, json=login_data, verify=False)
response.raise_for_status()

# Get the port forwarding rules
rules_url = f'{controller_url}/proxy/network/api/s/{site}/rest/portforward'
response = session.get(rules_url, verify=False)
response.raise_for_status()
rules = response.json()

# Find the rule to update
for rule in rules['data']:
    if rule['name'] == rule_name:
        rule_to_update = rule
        break

if rule_to_update is None:
    raise ValueError(f'No rule found with name: {rule_name}')

# Update the enable flag
rule_to_update['enabled'] = new_enable_value

# Send the update to the UniFi Controller
update_url = f'{controller_url}/proxy/network/api/s/{site}/rest/portforward/{rule_to_update["_id"]}'
response = session.put(update_url, json=rule_to_update, verify=False)
response.raise_for_status()

print(f"Rule '{rule_to_update['name']}' has been {'enabled' if new_enable_value else 'disabled'}.")

# Log out of the UniFi Controller
logout_url = f'{controller_url}/api/auth/logout'
session.post(logout_url, verify=False)


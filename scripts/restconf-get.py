import requests
import json

# set up connection parameters in a dictionary
router = {"ip": "devnetsandboxiosxe.cisco.com", "port": "443",
          "user": "admin", "password": "C1sco12345"}

# set REST API headers
headers = {"Accept": "application/yang-data+json",
           "Content-Type": "application/yang-data+json"}

url = f"https://{router['ip']}:{router['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1"
# print(url)

response = requests.get(url, headers=headers, auth=(
    router['user'], router['password']), verify=False)


api_data = response.json()
print("/" * 50)
print(api_data["Cisco-IOS-XE-interfaces-oper:interface"][0].get('interface-type'))
print("/" * 50)
if api_data["Cisco-IOS-XE-interfaces-oper:interface"][0].get("admin-status") == 'if-state-up':
    print('Interface is up')

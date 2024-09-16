import requests
import json

# set up connection parameters in a dictionary
router = {"ip": "devnetsandboxiosxe.cisco.com", "port": "443",
          "user": "admin", "password": "C1sco12345"}

# set REST API headers
headers = {"Accept": "application/yang-data+json",
           "Content-Type": "application/yang-data+json"}

url = f"https://{router['ip']}:{router['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/"
# print(url)

response = requests.get(url, headers=headers, auth=(
    router['user'], router['password']), verify=False)

#Estado de las interfaces
api_data = response.json()
interfaces = api_data["Cisco-IOS-XE-interfaces-oper:interfaces"]['interface']
for interface in interfaces:
    print('Name: ' + interface['name'])
    print('Description: ' + interface['description'])
    
    if interface['admin-status'] == 'if-state-up':
        print('Interface is up')
    else:
        print('Interface is down')
    print('/' * 20)

# url = f"https://{router['ip']}:{router['port']}/restconf/data/Cisco-IOS-XE-native:native/"
# response = requests.get(url, headers=headers, auth=(
#     router['user'], router['password']), verify=False)
# api_data = response.json()
# print(api_data['Cisco-IOS-XE-native:native']['ip']['route'])

with open('data/interface_data.json', 'w') as json_file:
    json.dump(api_data, json_file, indent = 4)
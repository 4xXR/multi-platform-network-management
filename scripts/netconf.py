from ncclient import manager
import json
import xmltodict

# Read configuration from file
with open('config/ios-xe_config.json') as config_file:
    config = json.load(config_file)

netconf_config = config['netconf']

# Device Configuration
host = netconf_config['host']
port = netconf_config['port']
username = netconf_config['username']
password = netconf_config['password']

# Create a NETCONF connection
with manager.connect(
    host=host,
    port=port,
    username=username,
    password=password,
    hostkey_verify=False
) as m:
       
    # Create an XML filter for targeted NETCONF queries
    netconf_filter = """
<filter>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
    </interfaces>
</filter>"""

    response = m.get_config(source='running', filter=netconf_config)
    interfaces = xmltodict.parse(response.xml)
    print(interfaces)

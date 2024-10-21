from datetime import datetime
import requests
import json
import os
import urllib3

urllib3.disable_warnings()

class Authentication():
    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, username, password):
        api = "/j_security_check"
        base_url = f"https://{vmanage_host}:{vmanage_port}"
        url = base_url + api
        payload = {'j_username': username, 'j_password': password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["set-Cookie"]
            jsessionid = cookies.split(";")[0]
            return jsessionid
        except KeyError:
            print("No valid JSESSION ID returned")
            exit()

    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = f"https://{vmanage_host}:{vmanage_port}"
        api = "/dataservice/client/token"
        url = base_url + api
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.text
        else:
            return None

#Load the device config
def load_device_config(file_path):
    with open(file_path,'r') as file_config:
        return json.load(file_config)

# # Function to obtain an authentication token
# def get_auth_token(device_config):
#     url = f"https://{device_config['ip']}:{device_config['port']}/j_security_check"
#     payload = {
#         "j_username": device_config['user'],
#         "j_password": device_config['password']
#     }
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     response = requests.post(url, data=payload, headers=headers, verify=False)

#     try:
#         session = requests.Session()
#         response = session.post(url, data=payload, verify=False)
#         if response.status_code == 200 and 'JSESSIONID' in session.cookies:
#             return session.cookies['JSESSIONID']
#         else:
#             print("Failed to obtain token. Check your credentials.")
#             return None
#     except requests.exceptions.RequestException as err:
#         print(f"Error occurred during token retrieval: {err}")
#         return None

#Get device data
def get_device_data(device_config, headers, endpoint, auth_type='basic'):
    url = f"https://{device_config['ip']}:{device_config['port']}/restconf/data/{endpoint}/"
    #url = f"https://{device_config['ip']}:{device_config['port']}/dataservice/device/tunnel/{endpoint}"
    try:
        if auth_type == 'token':
            headers['Cookie'] = f"JSESSIONID={device_config['token']}"
            response = requests.get(url, headers=headers, verify=False)
        else: # Assume basic authentication
            response = requests.get(url, headers=headers, auth=(device_config['user'], device_config['password']), verify=False)
        
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

#Save device data
def save_data_to_file(data,file_data_path):
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    with open(os.path.join(data_dir, file_data_path),'w') as file_data:
        json.dump(data,file_data,indent=4)

# set REST API headers and endpoint
# headers = {"Accept": "application/yang-data+json","Content-Type": "application/yang-data+json"}
# endpoint = 'Cisco-IOS-XE-interfaces-oper:interfaces/'

#Main function to coordinate the operation
def run_data_collection(device_config_file, endpoint):
    # Load the device configuration from the file
    device_config = load_device_config(device_config_file)
    
# Check for token-based authentication
    if device_config.get('auth_type') == 'token':
        Auth = Authentication()
        jsessionid = Auth.get_jsessionid(device_config['ip'], device_config['port'], device_config['user'], device_config['password'])
        token = Auth.get_token(device_config['ip'], device_config['port'], jsessionid)
        
        if token:
            headers = {
                "Accept": "application/yang-data+json",
                "Content-Type": "application/yang-data+json",
                "X-Auth-Token": token  # Agrega el token a los headers para la autenticación
            }
            auth_type = 'token'

        else:
            print("Error: No se pudo obtener el token de autenticación.")
            return  # Termina la ejecución si no se pudo obtener el token
    else:
        # Definir los headers RESTCONF para autenticación básica
        headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
        auth_type = 'basic'

        # Obtener los datos del dispositivo
    api_data = get_device_data(device_config,headers, endpoint, auth_type)
    
    # Obtener la fecha actual para nombrar el archivo de salida
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"interface_data_sdwan2{current_date}.json"
    
    # Guardar los datos en un archivo
    save_data_to_file(api_data, file_name)
    
    print(f"Data stored in: data/{file_name}")

#file_path = 'config/sdwan_config.json'
#device_config = load_device_config(file_path)
#print(device_config['ip'])
device_config_file = 'config/cat8000v_config.json'
endpoint = 'Cisco-IOS-XE-interfaces-oper:interface'
# Execute data collection
run_data_collection(device_config_file, endpoint)
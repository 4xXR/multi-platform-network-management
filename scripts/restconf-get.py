import datetime
import requests
import json
import os



#Load the device config
def load_device_config(file_path):
    with open(file_path,'r') as file_config:
        return json.load(file_config)
   
#Get device data
def get_device_data(device_config,headers, endpoint):
    url = f"https://{device_config['ip']}:{device_config['port']}/restconf/data/{endpoint}/"
    try:
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
    # Cargar configuración del dispositivo desde el archivo
    device_config = load_device_config(device_config_file)
    
    # Definir los headers RESTCONF
    headers = {"Accept": "application/yang-data+json",
               "Content-Type": "application/yang-data+json"}
    
    # Obtener los datos del dispositivo
    api_data = get_device_data(device_config,headers, endpoint)
    
    # Obtener la fecha actual para nombrar el archivo de salida
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"interface_data_{current_date}.json"
    
    # Guardar los datos en un archivo
    save_data_to_file(api_data, file_name)
    
    print(f"Datos guardados en: data/{file_name}")

# file_path = 'config/cat8000v_config.json'
# device_config = load_device_config(file_path)
# #print(device_config['ip'])
# global_device_config_file = run_data_collection(device_config_file)
# #Execute data collection
# run_data_collection(device_config_file, endpoint)
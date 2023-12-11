import json

import requests

url = 'http://localhost:9091/optimization'

json_data = json.load(open("../input_metadata/data_example_newer.json"))

response = requests.get('http://localhost:9091/')
print(response.json())

dict_ = {"optimization_request": json_data}

response = requests.post(f"{url}", json=dict_)
print(response.json())

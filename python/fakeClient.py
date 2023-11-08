import json

import requests

url = 'http://localhost:9091/optimization'
json_data = json.dumps(json.load(open("../input_data/data_kijowska_new.json")))
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json_data, headers=headers)
print(response)
print(response.content)

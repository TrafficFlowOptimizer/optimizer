import json
import os
from random import random

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get_root():
    return {"Hello": "World"}


@app.post('/post/')
def post_new_calculation(request: dict):
    json_string = json.dumps(request)

    idx = round(random() * 100)
    while os.path.exists(f'../input_data/{idx}.json'):
        idx = round(random() * 100)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(json_string)

    return {"success": True, "calculation idx": idx}


@app.get('/get/{id}')
def get_calculation_results(id: str):
    pass


@app.delete('/delete/{id}')
def delete_calculation(id: str):
    pass

import json
from random import random

import requests
from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def get_root():
    return {"Hello": "World"}

@app.post('/post/')
def post_new_calculation(request: dict):
    json_string = json.dumps(request)
    idx = round(random()*100)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(json_string)
    return {"success": True, "calculation idx": idx}

@app.get('/get/{id}')
def get_calculation_results(id: str):
    pass

@app.delete('/delete/{id}')
def delete_calculation(id: str):
    pass

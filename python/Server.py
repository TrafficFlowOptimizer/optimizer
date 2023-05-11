import json
import os
import random

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get_root():
    return {"Hello": "World"}


@app.post('/post/')
def post_new_calculation(request: dict):
    json_string = json.dumps(request)

    idx = random.randint(0, 999)
    while os.path.exists(f'../input_data/{idx}.json'):
        idx = random.randint(0, 999)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(json_string)

    with open(f'../minizinc/output/{idx}.txt', 'w') as f:
        f.write("*This is some default output*")

    return {"success": True, "calculation idx": idx}


@app.get('/get/{item_id}')
def get_calculation_results(item_id: int):
    try:
        with open(f'../minizinc/output/{item_id}.txt') as f:
            return {"success": True, "calculation results": f.read()}
    except FileNotFoundError:
        return {"success": False, "calculation results": "Invalid idx!"}


@app.delete('/delete/{item_id}')
def delete_calculation(item_id: int):
    file_not_exists = False
    if os.path.exists(f'../minizinc/output/{item_id}.txt'):
        os.remove(f'../minizinc/output/{item_id}.txt')
    else:
        file_not_exists = True

    if os.path.exists(f'../input_data/{item_id}.json'):
        os.remove(f'../input_data/{item_id}.json')
    else:
        file_not_exists = True

    if file_not_exists:
        return {"success": False, "deletion results": "Can't delete. File might not exist!"}

    return {"success": True, "deletion results": "Done!"}

@app.delete('/delete')
def delete_all():
    for item_id in range(1000):
        if os.path.exists(f'../minizinc/output/{item_id}.txt'):
            os.remove(f'../minizinc/output/{item_id}.txt')
        if os.path.exists(f'../input_data/{item_id}.json'):
            os.remove(f'../input_data/{item_id}.json')


    return {"success": True, "deletion results": "Done!"}

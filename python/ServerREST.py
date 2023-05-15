import asyncio
import json
import os
import random
import time

import uvicorn as uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from Optimizer import Optimizer

if __name__ == "__main__":
    uvicorn.run("Server:app", host="127.0.0.1", port=8000, reload=True)

    # print("new")
    # def tmp():
    #     uvicorn.run("Server:app", host="127.0.0.1", port=5000, reload=True)
    #     # os.system("uvicorn Server:app --reload")
    # observer = Observer()
    # observer.run()
    # t = Thread(target=tmp)
    # t.start()
    # t.join()
    #
    # print("4")

app = FastAPI()

async def my_async_function():
    # Your async code goes here
    await asyncio.sleep(5)
    return "Hello World"

@app.get("/")
async def my_get_function():
    result = await asyncio.create_task(my_async_function())
    return {"result": result}


@app.post('/post/')
async def post_new_calculation(request: dict):
    json_string = json.dumps(request)

    idx = random.randint(0, 999)
    while os.path.exists(f'../input_data/{idx}.json'):
        idx = random.randint(0, 999)
    with open(f'../input_data/{idx}.json', 'w') as f:
        f.write(json_string)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"calculation idx": idx})


@app.get('/get/{item_id}')
async def srg(item_id: int):
    return await asyncio.create_task(get_calculation_results(item_id))
    # return asyncio.create_task(get_calculation_results(item_id))
    # return f()

async def get_calculation_results(item_id: int):
    if os.path.exists(f'../input_data/{item_id}.json'):
        time_limit = 10
        print(item_id)
        timer = time.time()
        # observer.add_task(item_id)
        optimizer = Optimizer()
        optimizer.provide_data(f'../minizinc/data/{item_id}.dzn', item_id, 2)
        optimizer.solve(f'../minizinc/output/{item_id}.txt', time_limit)
        # await optimizer.solve(f'../minizinc/output/{item_id}.txt', time_limit)
        timer = time.time() - timer
        print("huh?")
        # optimizer.show_refactored_output(2)
        # print('{:.3f}'.format(timer), "seconds, ", end="")

        try:
            with open(f'../minizinc/output/{item_id}.txt') as f:
                if time_limit is not None and timer > time_limit:
                    return JSONResponse(status_code=status.HTTP_200_OK,
                                        content={"calculation results": f.read(),
                                                 "calculation time": "aborted due to time limit"})
                else:
                    return JSONResponse(status_code=status.HTTP_200_OK,
                                        content={"calculation results": f.read(),
                                                 "calculation time": "best solution found"})

        except FileNotFoundError:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"calculation results": "There is no output file. "
                                                                "Might be caused by problems with optimizer"})

    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"calculation results": "Invalid idx, can't find input data!"})
async def f():
    await asyncio.wait([get_calculation_results(757)])
    # return asyncio.run(get_calculation_results(757))
# f()
# asyncio.run(get_calculation_results(757))

@app.delete('/delete/{item_id}')
async def delete_calculation(item_id: int):
    file_not_exists = False
    if os.path.exists(f'../minizinc/output/{item_id}.txt'):
        os.remove(f'../minizinc/output/{item_id}.txt')
    else:
        file_not_exists = True

    if os.path.exists(f'../input_data/{item_id}.json'):
        os.remove(f'../input_data/{item_id}.json')
    else:
        file_not_exists = True

    if os.path.exists(f'../minizinc/data/{item_id}.dzn'):
        os.remove(f'../input_data/{item_id}.json')
    else:
        file_not_exists = True

    if file_not_exists:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"calculation results": "Can't delete. File might not exist!"})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"deletion results": "Done!"})


@app.delete('/delete')
async def delete_all():
    for item_id in range(1000):
        if os.path.exists(f'../minizinc/output/{item_id}.txt'):
            os.remove(f'../minizinc/output/{item_id}.txt')
        if os.path.exists(f'../input_data/{item_id}.json'):
            os.remove(f'../input_data/{item_id}.json')

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"deletion results": "Done!"})

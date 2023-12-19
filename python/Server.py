import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

from OptimizationRequest import OptimizationRequest, OptimizationRequestModel
from Optimizer import Optimizer
from Utils import clear

load_dotenv("../.env")

# server info
SERVER_HOST = os.getenv('SPRING_HOST')
SERVER_PORT = os.getenv('SPRING_PORT')
SERVER = "http://" + SERVER_HOST + ":" + SERVER_PORT + "/"

PASSWORD = os.getenv('PASSWORD')
PASSWORD_CODE = 'password'

# OT setup
HOST, PORT = os.getenv('OT_HOST'), int(os.getenv('OT_PORT'))
SOLVER = os.getenv('SOLVER')

app = FastAPI()


async def check_allowed_source(request: Request):
    if request.query_params.get(PASSWORD_CODE) != PASSWORD:
        raise HTTPException(status_code=403, detail="Forbidden: Source not allowed")


@app.middleware("http")
async def validate_source(request: Request, call_next):
    try:
        await check_allowed_source(request)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    response = await call_next(request)
    return response


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.post('/optimization')
def process_request(request: Request, optimization_request: OptimizationRequestModel):
    try:
        basic_optimizer = Optimizer(
            "../minizinc/models/basic_optimizer_newer.mzn",
            "../minizinc/models/basic_optimizer_newer_for_comparison.mzn"
        )
        optimization_request = OptimizationRequest(optimization_request.optimization_request)

        optimization_request.save_as_dzn(True)
        optimization_request.save_as_dzn(False)

        data = basic_optimizer.solve(optimization_request, SOLVER)
        # clear(optimization_request.idx)
    except Exception as error:
        print(error)
        return JSONResponse(
            content={"error_message": "Error occurred during optimization. Possibly invalid data."},
            status_code=500
        )

    print(data)
    if data is None:
        return JSONResponse(
            content={"error_message": "There are no optimization results for the given time"},
            status_code=422
        )

    return JSONResponse(content=data, status_code=200)


if __name__ == "__main__":
    # clear()
    uvicorn.run("Server:app", port=PORT, host="0.0.0.0", reload=True)

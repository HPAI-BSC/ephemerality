from fastapi import FastAPI
from api11 import get_all_ephemeralities, get_left_core_ephemerality, get_middle_core_ephemerality, get_right_core_ephemerality, get_sorted_core_ephemerality


app = FastAPI()


@app.post("/{api_version}/all", status_code=201)
async def get_all_ephemeralities():
    pass

@app.post("/{api_version}/left", status_code=201)
async def get_all_ephemeralities():
    pass

@app.post("/{api_version}/middle", status_code=201)
async def get_all_ephemeralities():
    pass

@app.post("/{api_version}/right", status_code=201)
async def get_all_ephemeralities():
    pass

@app.post("/{api_version}/sorted", status_code=201)
async def get_all_ephemeralities():
    pass
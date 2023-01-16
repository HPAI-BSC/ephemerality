from fastapi import FastAPI, status
from pydantic import BaseModel
import rest.api11 as api11
from src import EphemeralitySet


app = FastAPI()


class InputData(BaseModel):
    input_vector: list[float]
    threshold: float


@app.post("/ephemerality/{api_version}/all", status_code=status.HTTP_200_OK)
async def get_all_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_all_ephemeralities(input_vector=input_data.input_vector, threshold=input_data.threshold)
    else:
        raise ValueError(f'Unrecognized API version: {api_version}!')

@app.post("/ephemerality/{api_version}/left", status_code=status.HTTP_200_OK)
async def get_left_core_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_left_core_ephemerality(input_vector=input_data['input_vector'], threshold=input_data['threshold'])
    else:
        raise ValueError(f'Unrecognized API version: {api_version}!')

@app.post("/ephemerality/{api_version}/middle", status_code=status.HTTP_200_OK)
async def get_middle_core_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_middle_core_ephemerality(input_vector=input_data['input_vector'], threshold=input_data['threshold'])
    else:
        raise ValueError(f'Unrecognized API version: {api_version}!')

@app.post("/ephemerality/{api_version}/right", status_code=status.HTTP_200_OK)
async def get_right_core_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_right_core_ephemerality(input_vector=input_data['input_vector'], threshold=input_data['threshold'])
    else:
        raise ValueError(f'Unrecognized API version: {api_version}!')

@app.post("/ephemerality/{api_version}/sorted", status_code=status.HTTP_200_OK)
async def get_sorted_core_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_sorted_core_ephemerality(input_vector=input_data['input_vector'], threshold=input_data['threshold'])
    else:
        raise ValueError(f'Unrecognized API version: {api_version}!')
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Any, Sequence
import rest.api11 as api11
from ephemerality import EphemeralitySet


app = FastAPI()


class InputData(BaseModel):
    """
    POST request body format
    """
    input_sequence: list[str]
    input_type: str = 'frequencies'  # 'frequencies' | 'f' | 'timestamps' | 't'
    threshold: float = 0.8
    range: None | tuple[str, str] = None  # used only if input_type == 'timestamps', defaults to (min(timestamps), max(timestamps) + 1)
    granularity: None | str = 'day'  # used only if input_type == 'timestamps'; ['week', 'day', 'hour']


@app.post("/ephemerality/{api_version}/all", status_code=status.HTTP_200_OK)
async def get_all_ephemeralities(api_version: str, input_data: InputData) -> EphemeralitySet:
    if api_version == '1.1':
        return api11.get_all_ephemeralities(input_vector=input_data.input_sequence, threshold=input_data.threshold)
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
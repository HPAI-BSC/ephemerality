from fastapi import APIRouter, status, Query, Response
from fastapi.responses import JSONResponse
from typing import Annotated, Any, Union
import sys
import time
import rest
from ephemerality import InputData, process_input
from memory_profiler import memory_usage


TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == 'test'
router = APIRouter()


def set_test_mode(mode: bool) -> None:
    global TEST_MODE
    TEST_MODE = mode


def run_computations(input_data: list[InputData], core_types: str, api: rest.AbstractRestApi, include_input: bool = False)\
        -> Union[list[dict[str, Any] | dict[str, dict[str, Any]]], None]:
    output = []
    for test_case in input_data:
        vector, threshold = process_input(input_remote_data=test_case)
        case_output = api.get_ephemerality(input_vector=vector, threshold=threshold, types=core_types).dict(exclude_none=True)
        if include_input:
            output.append({
                "input": test_case.dict(),
                "output": case_output
            })
        else:
            output.append(case_output)
    return output


@router.post("/ephemerality/{api_version}/all", status_code=status.HTTP_200_OK)
async def compute_all_ephemeralities(
        input_data: list[InputData],
        core_types: Annotated[
            str, Query(min_length=1, max_length=4, regex="^[lmrs]+$")
        ] = "lmrs",
        api_version: str | None = None,
        test_time_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        test_ram_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        include_input: bool = True,
        explanations: bool = True
) -> Response:

    if api_version is None:
        api = rest.DEFAULT_API
    elif api_version not in rest.API_VERSION_DICT:
        raise ValueError(f'Unrecognized API version: {api_version}!')
    else:
        api = rest.API_VERSION_DICT[api_version]

    if TEST_MODE and (test_time_reps or test_ram_reps):
        output = {}
        if test_time_reps:
            times = []
            for i in range(test_time_reps):
                start_time = time.time()
                run_computations(input_data=input_data, core_types=core_types, api=api)
                times.append(time.time() - start_time)
            output["time"] = times
        if test_ram_reps:
            rams = []
            for i in range(test_ram_reps):
                rams.append(memory_usage(
                    (run_computations, [], {"input_data": input_data, "core_types": core_types, "api": api}),
                    max_usage=True
                )[0])
            output["RAM"] = rams

        return JSONResponse(content=output)
    else:
        output = run_computations(input_data=input_data, core_types=core_types, api=api, include_input=include_input)
        return JSONResponse(content=output)

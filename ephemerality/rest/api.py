import sys
import time
from typing import Annotated, Any, Union

import ephemerality.rest as rest
from ephemerality.src import InputData, process_input
from fastapi import APIRouter, status, Query, Response
from fastapi.responses import JSONResponse
from memory_profiler import memory_usage

TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == 'test'
router = APIRouter()


def set_test_mode(mode: bool) -> None:
    global TEST_MODE
    TEST_MODE = mode


def run_computations(input_data: list[InputData], core_types: str, api: rest.AbstractRestApi, include_input: bool = False)\
        -> Union[list[dict[str, Any] | dict[str, dict[str, Any]]], None]:
    output = []
    noname_counter = 0
    for test_case in input_data:
        case_input = process_input(input_remote_data=test_case)[0]
        case_output = api.get_ephemerality(
            input_vector=case_input.activity,
            threshold=case_input.threshold,
            types=core_types
        ).dict(exclude_none=True)

        if include_input:
            output.append({
                "input": test_case.dict(),
                "output": case_output
            })
        else:
            if test_case.reference_name:
                input_name = test_case.reference_name
            else:
                input_name = str(noname_counter)
                noname_counter += 1

            output.append({
                "input": input_name,
                "output": case_output
            })
    return output


def process_request(
        input_data: list[InputData],
        api_version: str,
        core_types: str,
        test_time_reps: int | None,
        test_ram_reps: int | None,
        include_input: bool,
        explanations: bool
) -> Response:
    if api_version not in rest.API_VERSION_DICT:
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
                ))
            output["RAM"] = rams

        return JSONResponse(content=output)
    else:
        output = run_computations(input_data=input_data, core_types=core_types, api=api, include_input=include_input)
        return JSONResponse(content=output)


@router.post("/ephemerality/all", status_code=status.HTTP_200_OK)
async def compute_all_ephemeralities_default_version(
        input_data: list[InputData],
        core_types: Annotated[
            str, Query(min_length=1, max_length=4, regex="^[lmrs]+$")
        ] = "lmrs",
        test_time_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        test_ram_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        include_input: bool = False,
        explanations: bool = False
) -> Response:
    default_version = rest.DEFAULT_API.version()
    return process_request(
        input_data=input_data,
        core_types=core_types,
        api_version=default_version,
        test_time_reps=test_time_reps,
        test_ram_reps=test_ram_reps,
        include_input=include_input,
        explanations=explanations
    )


@router.post("/ephemerality/{api_version}/all", status_code=status.HTTP_200_OK)
async def compute_all_ephemeralities(
        input_data: list[InputData],
        api_version: str,
        core_types: Annotated[
            str, Query(min_length=1, max_length=4, regex="^[lmrs]+$")
        ] = "lmrs",
        test_time_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        test_ram_reps: Annotated[
            int | None, Query(ge=1)
        ] = None,
        include_input: bool = False,
        explanations: bool = False
) -> Response:

    return process_request(
        input_data=input_data,
        core_types=core_types,
        api_version=api_version,
        test_time_reps=test_time_reps,
        test_ram_reps=test_ram_reps,
        include_input=include_input,
        explanations=explanations
    )

import numpy as np
from datetime import datetime, timezone, timedelta
from pathlib import Path
from pydantic import BaseModel
from typing import Sequence
import json
import warnings


SECONDS_WEEK = 604800.
SECONDS_DAY = 86400.
SECONDS_HOUR = 3600.


class InputData(BaseModel):
    """
    POST request body format
    """
    input: list[str]
    input_type: str = 'f'  # 'frequencies' | 'f' | 'timestamps' | 't' | 'datetime' | 'd'
    threshold: float = 0.8
    time_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"  # used only if input_type == 'datetime' | 'd'. Should be in strptime format
    timezone: float = 0.  # used only if input_type == 'datetime' | 'd'. Offset in hours from the UTC time. Should be within [-24, +24] range.
    range: None | tuple[str, str] = None  # used only if input_type == 'timestamps' | 't', defaults to (min(timestamps), max(timestamps) + 1)
    granularity: None | str = 'day'  # used only if input_type == 'timestamps' | 't'. {'week', 'day', 'hour', '_d', '_h'}


def process_input(
        input_folder: str | Path | None = None,
        recursive: bool = True,
        input_file: str | Path | None = None,
        input_remote_data: InputData | None = None,
        input_dict: dict | None = None,
        input_seq: Sequence[float | int | str] | None = None,
        threshold: float=0.8) -> list[tuple[np.ndarray[float], float]]:
    output = []

    if input_folder:
        output.extend(process_folder(path=Path(input_folder), recursive=recursive, threshold=threshold))

    if input_file:
        output.extend(process_file(path=Path(input_file), threshold=threshold))

    if input_remote_data:
        output.extend(process_formatted_data(input_remote_data))

    if input_dict:
        output.extend(process_formatted_data(InputData(**input_dict)))

    if input_seq:
        if threshold is None:
            raise ValueError('Threshold value is not defined!')
        output.append((np.ndarray(input_seq, dtype=float), threshold))

    return output

def process_folder(path: Path, recursive: bool = True, threshold: float | None = None) -> list[tuple[np.ndarray[float], float]]:
    output = []
    for file in path.iterdir():
        if file.is_file():
            output.extend(process_file(path=file, threshold=threshold))
        elif file.is_dir() and recursive:
            output.extend(process_folder(path=file, recursive=recursive, threshold=threshold))
    return output


def process_file(path: Path, threshold: float | None = None) -> list[tuple[np.ndarray[float], float]]:
    if path.suffix == '.json':
        return process_json(path)
    elif path.suffix == '.csv':
        return [(sequence, threshold) for sequence in process_csv(path)]
    else:
        return []


def process_json(path: Path) -> list[tuple[np.ndarray[float], float]]:
    with open(path, 'r') as f:
        input_object = json.load(f)

    if isinstance(input_object, dict):
        input_object = [input_object]

    output = []
    for input_case in input_object:
        input_case = InputData(**input_case)
        try:
            process_formatted_data(input_case)
        except ValueError:
            warnings.warn(f'\"input_type\" is not one of ["frequencies", "f", "timestamps", "t"]! Ignoring file \"{str(path.absolute())}\"!')

    return output


def process_formatted_data(input_data: InputData) -> tuple[np.ndarray[float], float]:
    if input_data.input_type == 'frequencies' or input_data.input_type == 'f':
        return np.array(input_data.input), input_data.threshold
    elif input_data.input_type == 'timestamps' or input_data.input_type == 't':
        return timestamps_to_frequencies(np.array(input_data.input, dtype=float), input_data.range,
                                         input_data.granularity), input_data.threshold
    elif input_data.input_type == 'datetime' or input_data.input_type == 'd':
        timestamps = [datetime.strptime(time_point, input_data.time_format).replace(tzinfo=timezone(timedelta(hours=input_data.timezone))).timestamp()
                      for time_point in input_data.input]
        return timestamps_to_frequencies(np.array(timestamps, dtype=float), input_data.range,
                                         input_data.granularity), input_data.threshold
    else:
        raise ValueError("Wrong \"input_type\" value!")


def process_csv(path: Path) -> list[np.ndarray[float]]:
    output = []
    with open(path, 'r') as f:
        for line in f:
            if line:
                output.append(np.fromstring(line.strip(), dtype=float, sep=','))
    return output


def timestamps_to_frequencies(timestamps: Sequence[float | int | str],
                              ts_range: None | tuple[float | int | str, float | int | str] = None,
                              granularity: str = 'day') -> np.ndarray[float]:
    if not isinstance(timestamps, np.ndarray) or timestamps.dtype != float:
        timestamps = np.array(timestamps, dtype=float)
    if ts_range is None:
        ts_range = (np.min(timestamps), np.max(timestamps))
    if granularity == 'week':
        bin_width = SECONDS_WEEK
    elif granularity == 'day':
        bin_width = SECONDS_DAY
    elif granularity == 'hour':
        bin_width = SECONDS_HOUR
    elif granularity[-1] == 'd' and _is_float(granularity[:-1]):
        bin_width = float(granularity[:-1]) * SECONDS_DAY
    elif granularity[-1] == 'h' and _is_float(granularity[:-1]):
        bin_width = float(granularity[:-1]) * SECONDS_HOUR
    else:
        raise ValueError(f"Invalid granularity value: {granularity}!")

    bins = np.arange(ts_range[0], ts_range[1], bin_width)
    if not np.isclose(bins[-1], ts_range[1]):
        bins = np.append(bins, ts_range[1])

    frequency, _ = np.histogram(np.array(timestamps, dtype=float), bins=bins)
    return frequency


def _is_float(num: str) -> bool:
    try:
        tmp = float(num)
    except ValueError:
        return False
    return True

import numpy as np
from datetime import datetime
from typing import Sequence
from rest import InputData


def process_input_raw(input_body: InputData) -> tuple(np.ndarray, float):
    if input_body.input_type == 'frequencies' or input_body.input_type == 'f':
        return input_body.input_sequence, input_body.threshold
    elif input_body.input_type == 'timestamps' or input_body.input_type == 't':
        return timestamps_to_frequencies(input_body.input_sequence, input_body.range, input_body.granularity),\
               input_body.threshold
    else:
        raise ValueError('input_type is not one of ["frequencies", "f", "timestamps", "t"]!')


def timestamps_to_frequencies(timestamps: Sequence[float | int | str],
                              range: None | tuple[float | int | str, float | int | str] = None,
                              granularity: str = 'day') -> np.ndarray[float]:
    pass
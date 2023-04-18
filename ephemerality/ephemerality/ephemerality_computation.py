import numpy as np
from typing import Sequence
from ephemerality.utils import ResultSet


def _check_threshold(threshold: float) -> bool:
    if threshold <= 0.:
        raise ValueError('Threshold value must be greater than 0!')

    if threshold > 1.:
        raise ValueError('Threshold value must be less or equal to 1!')

    return True


def _ephemerality_raise_error(threshold: float):
    if _check_threshold(threshold):
        raise ValueError('Input activity vector has not been internally normalized (problematic data format?)!')


def _normalize_activity_vector(activity_vector: Sequence[float]) -> np.array:
    activity_vector = np.array(activity_vector)

    if sum(activity_vector) != 1.:
        activity_vector /= np.sum(activity_vector)
        
    return activity_vector


def compute_left_core_length(activity_vector: np.array, threshold: float) -> int:
    current_sum = 0
    for i, freq in enumerate(activity_vector):
        current_sum = current_sum + freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def compute_right_core_length(activity_vector: np.array, threshold: float) -> int:
    current_sum = 0
    for i, freq in enumerate(activity_vector[::-1]):
        current_sum = current_sum + freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def compute_middle_core_length(activity_vector: np.array, threshold: float) -> int:
    lower_threshold = (1. - threshold) / 2

    current_left_sum = 0
    start_index = -1
    for i, freq in enumerate(activity_vector):
        current_left_sum += freq
        if current_left_sum > lower_threshold and not np.isclose(current_left_sum, lower_threshold):
            start_index = i
            break

    current_sum = 0
    for j, freq in enumerate(activity_vector[start_index:]):
        current_sum += freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return j + 1

    _ephemerality_raise_error(threshold)


def compute_sorted_core_length(activity_vector: np.array, threshold: float) -> int:
    freq_descending_order = np.sort(activity_vector)[::-1]

    current_sum = 0
    for i, freq in enumerate(freq_descending_order):
        current_sum += freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def _compute_ephemerality_from_core(core_length: int, range_length: int, threshold: float):
    return max(0., 1 - (core_length / range_length) / threshold)


def compute_ephemerality(
        activity_vector: Sequence[float],
        threshold: float = 0.8,
        types: str = 'lmrs') -> ResultSet:

    _check_threshold(threshold)

    if np.sum(activity_vector) == 0.:
        raise ZeroDivisionError("Activity vector's sum is 0!")
    
    activity_vector = _normalize_activity_vector(activity_vector)
    range_length = len(activity_vector)

    if 'l' in types:
        length_left_core = compute_left_core_length(activity_vector, threshold)
        ephemerality_left_core = _compute_ephemerality_from_core(length_left_core, range_length, threshold)
    else:
        length_left_core = None
        ephemerality_left_core = None

    if 'm' in types:
        length_middle_core = compute_middle_core_length(activity_vector, threshold)
        ephemerality_middle_core = _compute_ephemerality_from_core(length_middle_core, range_length, threshold)
    else:
        length_middle_core = None
        ephemerality_middle_core = None

    if 'r' in types:
        length_right_core = compute_right_core_length(activity_vector, threshold)
        ephemerality_right_core = _compute_ephemerality_from_core(length_right_core, range_length, threshold)
    else:
        length_right_core = None
        ephemerality_right_core = None

    if 's' in types:
        length_sorted_core = compute_sorted_core_length(activity_vector, threshold)
        ephemerality_sorted_core = _compute_ephemerality_from_core(length_sorted_core, range_length, threshold)
    else:
        length_sorted_core = None
        ephemerality_sorted_core = None

    ephemeralities = ResultSet(
        len_left_core=length_left_core,
        len_middle_core=length_middle_core,
        len_right_core=length_right_core,
        len_sorted_core=length_sorted_core,

        eph_left_core=ephemerality_left_core,
        eph_middle_core=ephemerality_middle_core,
        eph_right_core=ephemerality_right_core,
        eph_sorted_core=ephemerality_sorted_core
    )

    return ephemeralities

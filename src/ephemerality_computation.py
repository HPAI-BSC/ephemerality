import numpy as np
from typing import Sequence
from dataclasses import dataclass, asdict
import warnings


@dataclass
class Ephemerality:
    """CLass to contain ephemerality values by subtypes"""
    left_core: float = 1.
    middle_core: float = 1.
    right_core: float = 1.
    sorted_core: float = 1

    @property
    def dict(self):
        return self.__dict__.copy()



def _normalize_frequency_vector(frequency_vector: Sequence[float]) -> np.array:
    frequency_vector = np.array(frequency_vector)

    if sum(frequency_vector) != 1.:
        frequency_vector /= np.sum(frequency_vector)
        
    return frequency_vector


def _ephemerality_raise_error(threshold: float):
    if 0. < threshold <= 1:
        raise ValueError('Input frequency vector has not been internally normalized!')
    else:
        raise ValueError('Threshold value is not within (0, 1] range!')


def compute_left_core_length(frequency_vector: np.array, threshold: float) -> int:
    current_sum = 0
    for i, freq in enumerate(frequency_vector):
        current_sum = current_sum + freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def compute_right_core_length(frequency_vector: np.array, threshold: float) -> int:
    current_sum = 0
    for i, freq in enumerate(frequency_vector[::-1]):
        current_sum = current_sum + freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def compute_middle_core_length(frequency_vector: np.array, threshold: float) -> int:
    lower_threshold = (1. - threshold) / 2

    current_presum = 0
    start_index = -1
    for i, freq in enumerate(frequency_vector):
        current_presum += freq
        if current_presum > lower_threshold and not np.isclose(current_presum, lower_threshold):
            start_index = i
            break

    current_sum = 0
    for j, freq in enumerate(frequency_vector[start_index:]):
        current_sum += freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return j + 1

    _ephemerality_raise_error(threshold)


def compute_sorted_core_length(frequency_vector: np.array, threshold: float) -> int:
    freq_descending_order = np.sort(frequency_vector)[::-1]

    current_sum = 0
    for i, freq in enumerate(freq_descending_order):
        current_sum += freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    _ephemerality_raise_error(threshold)


def _compute_ephemerality_from_core(core_length: int, range_length: int, threshold: float):
    return 1 - (core_length / range_length) / threshold


def compute_ephemerality(
        frequency_vector: Sequence[float],
        threshold: float = 0.8) -> dict[str, float]:

    if threshold <= 0.:
        raise ValueError('Threshold value must be greater than 0!')

    if threshold > 1.:
        raise ValueError('Threshold value must be less or equal to 1!')

    if np.isclose(np.sum(frequency_vector), 0.):
        return Ephemerality().dict
    
    frequency_vector = _normalize_frequency_vector(frequency_vector)
    range_length = len(frequency_vector)

    left_core_length = compute_left_core_length(frequency_vector, threshold)
    ephemerality_left_core = _compute_ephemerality_from_core(left_core_length, range_length, threshold)
    if ephemerality_left_core < 0. and not np.isclose(ephemerality_left_core, 0.):
        warnings.warn(f'Original ephemerality value is less than 0 ({ephemerality_left_core}) and is going to be rounded up! '
                      f'This is indicative of the edge case in which ephemerality span is greater than '
                      f'[threshold * input_vector_length], i.e. most of the frequency mass lies in a few vector '
                      f'elements at the end of the frequency vector. Original ephemerality in this case should be '
                      f'considered to be equal to 0. However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_left_core = 0.

    middle_core_length = compute_middle_core_length(frequency_vector, threshold)
    ephemerality_middle_core = _compute_ephemerality_from_core(middle_core_length, range_length, threshold)
    if ephemerality_middle_core < 0. and not np.isclose(ephemerality_middle_core, 0.):
        warnings.warn(f'Filtered ephemerality value is less than 0 ({ephemerality_middle_core}) and is going to be rounded up! '
                      f'This is indicative of the edge case in which ephemerality span is greater than '
                      f'[threshold * input_vector_length], i.e. most of the frequency mass lies in a few elements '
                      f'at the beginning and the end of the frequency vector. Filtered ephemerality in this case should '
                      f'be considered to be equal to 0. However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_middle_core = 0.

    right_core_length = compute_right_core_length(frequency_vector, threshold)
    ephemerality_right_core = _compute_ephemerality_from_core(right_core_length, range_length, threshold)
    if ephemerality_right_core < 0. and not np.isclose(ephemerality_right_core, 0.):
        warnings.warn(f'Original ephemerality value is less than 0 ({ephemerality_right_core}) and is going to be rounded up! '
                      f'This is indicative of the edge case in which ephemerality span is greater than '
                      f'[threshold * input_vector_length], i.e. most of the frequency mass lies in a few vector '
                      f'elements at the end of the frequency vector. Original ephemerality in this case should be '
                      f'considered to be equal to 0. However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_right_core = 0.

    sorted_core_length = compute_sorted_core_length(frequency_vector, threshold)
    ephemerality_sorted_core = _compute_ephemerality_from_core(sorted_core_length, range_length, threshold)
    if ephemerality_sorted_core < 0. and not np.isclose(ephemerality_sorted_core, 0.):
        warnings.warn(f'Sorted ephemerality value is less than 0 ({ephemerality_sorted_core}) and is going to be rounded up! '
                      f'This is indicative of the rare edge case of very short and mostly uniform frequency vector (so '
                      f'that ephemerality span is greater than [threshold * input_vector_length]). '
                      f'Sorted ephemerality in this case should be considered to be equal to 0. '
                      f'However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_sorted_core = 0.

    ephemeralities = Ephemerality(left_core=ephemerality_left_core,
                                  middle_core=ephemerality_middle_core,
                                  right_core=ephemerality_right_core,
                                  sorted_core=ephemerality_sorted_core)

    return ephemeralities.dict

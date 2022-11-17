import numpy as np
from typing import Sequence
import warnings


def _normalize_frequency_vector(frequency_vector: Sequence[float]) -> np.array:
    frequency_vector = np.array(frequency_vector)

    if sum(frequency_vector) != 1.:
        frequency_vector /= np.sum(frequency_vector)
        
    return frequency_vector


def ephemerality_raise_error(threshold: float):
    if 0. < threshold <= 1:
        raise ValueError('Input frequency vector has not been internally normalized!')
    else:
        raise ValueError('Threshold value is not within (0, 1] range!')


def compute_ephemerality_original_span(frequency_vector: np.array, threshold: float) -> int:
    current_sum = 0
    for i, freq in enumerate(frequency_vector):
        current_sum = current_sum + freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    ephemerality_raise_error(threshold)


def compute_ephemerality_filtered_span(frequency_vector: np.array, threshold: float) -> int:
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

    ephemerality_raise_error(threshold)


def compute_ephemerality_sorted_span(frequency_vector: np.array, threshold: float) -> int:
    freq_descending_order = np.sort(frequency_vector)[::-1]

    current_sum = 0
    for i, freq in enumerate(freq_descending_order):
        current_sum += freq
        if np.isclose(current_sum, threshold) or current_sum > threshold:
            return i + 1

    ephemerality_raise_error(threshold)


def compute_ephemerality_from_span(span: int, range_length: int, threshold: float):
    return 1 - (span / range_length) / threshold


def compute_ephemeralities(
        frequency_vector: Sequence[float],
        threshold: float = 0.8) -> dict[str, float]:

    if threshold <= 0.:
        raise ValueError('Threshold value must be greater than 0!')

    if threshold > 1.:
        raise ValueError('Threshold value must be less or equal to 1!')

    if np.isclose(np.sum(frequency_vector), 0.):
        return {
            'ephemerality_original': 1.,
            'ephemerality_original_span': 0,
            'ephemerality_filtered': 1.,
            'ephemerality_filtered_span': 0,
            'ephemerality_sorted': 1.,
            'ephemerality_sorted_span': 0
        }
    
    frequency_vector = _normalize_frequency_vector(frequency_vector)
    range_length = len(frequency_vector)

    ephemerality_original_span = compute_ephemerality_original_span(frequency_vector, threshold)
    ephemerality_original = compute_ephemerality_from_span(ephemerality_original_span, range_length, threshold)

    # print(f'Orig: {ephemerality_original}, {ephemerality_original_span}')

    if ephemerality_original < 0. and not np.isclose(ephemerality_original, 0.):
        warnings.warn(f'Original ephemerality value is less than 0 ({ephemerality_original}) and is going to be rounded up! '
                      f'This is indicative of the edge case in which ephemerality span is greater than '
                      f'[threshold * input_vector_length], i.e. most of the frequency mass lies in a few vector '
                      f'elements at the end of the frequency vector. Original ephemerality in this case should be '
                      f'considered to be equal to 0. However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_original = 0.

    ephemerality_filtered_span = compute_ephemerality_filtered_span(frequency_vector, threshold)
    ephemerality_filtered = compute_ephemerality_from_span(ephemerality_filtered_span, range_length, threshold)
    if ephemerality_filtered < 0. and not np.isclose(ephemerality_filtered, 0.):
        warnings.warn(f'Filtered ephemerality value is less than 0 ({ephemerality_filtered}) and is going to be rounded up! '
                      f'This is indicative of the edge case in which ephemerality span is greater than '
                      f'[threshold * input_vector_length], i.e. most of the frequency mass lies in a few elements '
                      f'at the beginning and the end of the frequency vector. Filtered ephemerality in this case should '
                      f'be considered to be equal to 0. However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_filtered = 0.

    ephemerality_sorted_span = compute_ephemerality_sorted_span(frequency_vector, threshold)
    ephemerality_sorted = compute_ephemerality_from_span(ephemerality_sorted_span, range_length, threshold)
    if ephemerality_sorted < 0. and not np.isclose(ephemerality_sorted, 0.):
        warnings.warn(f'Sorted ephemerality value is less than 0 ({ephemerality_sorted}) and is going to be rounded up! '
                      f'This is indicative of the rare edge case of very short and mostly uniform frequency vector (so '
                      f'that ephemerality span is greater than [threshold * input_vector_length]). '
                      f'Sorted ephemerality in this case should be considered to be equal to 0. '
                      f'However, please double check the input vector!',
                      RuntimeWarning)
        ephemerality_sorted = 0.

    ephemeralities = {
        'ephemerality_original': ephemerality_original,
        'ephemerality_original_span': ephemerality_original_span,
        'ephemerality_filtered': ephemerality_filtered,
        'ephemerality_filtered_span': ephemerality_filtered_span,
        'ephemerality_sorted': ephemerality_sorted,
        'ephemerality_sorted_span': ephemerality_sorted_span
    }

    return ephemeralities

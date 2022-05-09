import numpy as np
from typing import Sequence, Dict


def compute_ephemerality_measures(
        frequency_vector: Sequence[float],
        threshold: float = 0.8) -> Dict[str, float]:
    frequency_vector = np.array(frequency_vector)
    if sum(frequency_vector) != 1.:
        frequency_vector /= np.sum(frequency_vector)
    cumulative_distribution_function = np.cumsum(frequency_vector)

    lower_threshold = (1. - threshold) / 2
    upper_threshold = 1 - lower_threshold
    eph_10 = (cumulative_distribution_function >= lower_threshold).argmax()
    eph_90 = (cumulative_distribution_function >= upper_threshold).argmax()
    topic_range = len(frequency_vector) - 1
    first_freq_index_above_zero = (frequency_vector > 0.).argmax()
    last_freq_index_above_zero = topic_range - np.flip(frequency_vector > 0.).argmax()
    topic_activity_range = last_freq_index_above_zero - first_freq_index_above_zero + 1

    ephemerality_2_range = eph_90 - eph_10 + 1
    ephemerality_2 = 1 - (ephemerality_2_range / topic_activity_range)

    freq_descending_order = np.sort(frequency_vector)[::-1]
    aux_cdf = np.cumsum(freq_descending_order)
    eph4_80 = (aux_cdf >= threshold).argmax() + 1
    eph4_range = (freq_descending_order > 0.).argmin() + 1
    ephemerality_4 = 1 - ((1 / 0.8) * (eph4_80 / eph4_range))

    ephemeralities = {
        "ephemerality2": round(ephemerality_2, 2),
        "ephemerality4": round(ephemerality_4, 2)
    }

    return ephemeralities

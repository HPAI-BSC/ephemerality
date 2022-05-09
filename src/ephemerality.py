import numpy as np


def compute_ephemerality_measures(frequency_vector: np.array(float), eph1_threshold: float = 0.8):
    cumulative_distribution_function = np.cumsum(frequency_vector)

    eph_10 = (cumulative_distribution_function >= 0.1).argmax()
    eph_80 = (cumulative_distribution_function >= eph1_threshold).argmax()
    eph_90 = (cumulative_distribution_function >= 0.9).argmax()
    topic_range = len(frequency_vector) - 1
    first_freq_index_above_zero = (frequency_vector > 0.).argmax()
    last_freq_index_above_zero = topic_range - np.flip(frequency_vector > 0.).argmax()
    topic_activity_range = last_freq_index_above_zero - first_freq_index_above_zero

    ephemerality_1_range = eph_80 - first_freq_index_above_zero
    ephemerality_1 = 1 - (ephemerality_1_range / topic_activity_range)

    ephemerality_2_range = eph_90 - eph_10
    ephemerality_2 = 1 - (ephemerality_2_range / topic_activity_range)

    freq_descending_order = np.sort(frequency_vector)[::-1]
    aux_cdf = np.cumsum(freq_descending_order)
    eph4_80 = (aux_cdf >= eph1_threshold).argmax()
    ephemerality_4 = 1 - ((1 / 0.8) * (eph4_80 / topic_activity_range))

    ephemeralities = {
        "eph1": round(ephemerality_1, 2),
        "eph2": round(ephemerality_2, 2),
        "eph4": round(ephemerality_4, 2)
    }
    return ephemeralities

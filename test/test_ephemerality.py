from unittest import TestCase

import numpy as np

from src.ephemerality import compute_ephemerality_measures


class TestComputeEphemerality(TestCase):
    def test_compute_ephemerality_measures(self):
        input_frequency_vector = np.array([0, 0, 0, 0, 0])
        expected_ephemeralities = {'eph1': 1.0, 'eph2': 1.0, 'eph4': 1.0}
        actual_ephemeralities = compute_ephemerality_measures(input_frequency_vector)
        self.assertEqual(expected_ephemeralities, actual_ephemeralities)

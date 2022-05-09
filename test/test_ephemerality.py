from unittest import TestCase

from src import compute_ephemerality_measures


class TestComputeEphemerality(TestCase):
    def test_compute_ephemerality_measures(self):
        input_frequency_vector = [0., 0., 0., .2, .55, 0., 0.15, .1, 0., 0.]
        expected_ephemeralities = {'ephemerality2': 0.2, 'ephemerality4': 0.25}
        actual_ephemeralities = compute_ephemerality_measures(input_frequency_vector)
        self.assertEqual(expected_ephemeralities, actual_ephemeralities)

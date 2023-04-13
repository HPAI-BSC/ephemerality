from unittest import TestCase
import numpy as np
from testing.test_utils import EphemeralityTestCase
from ephemerality import compute_ephemerality, ResultSet


TEST_CASES = [
    EphemeralityTestCase(
        input_sequence=[1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=2,
            len_sorted_core=1,
            eph_left_core=0.375,
            eph_middle_core=0.375,
            eph_right_core=0.,
            eph_sorted_core=0.375
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=2,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.375,
            eph_right_core=0.375,
            eph_sorted_core=0.375
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[.5, .5],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=2,
            len_right_core=2,
            len_sorted_core=2,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[.5, .5],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0.7, .3],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=2,
            len_right_core=2,
            len_sorted_core=2,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0.7, .3],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=4,
            len_sorted_core=1,
            eph_left_core=0.6875,
            eph_middle_core=0.6875,
            eph_right_core=0.,
            eph_sorted_core=0.6875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=4,
            len_sorted_core=1,
            eph_left_core=1 / 6,
            eph_middle_core=1 / 6,
            eph_right_core=0.,
            eph_sorted_core=1 / 6
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.6875,
            eph_right_core=0.6875,
            eph_sorted_core=0.6875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=1 / 6,
            eph_right_core=1 / 6,
            eph_sorted_core=1 / 6
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 1., 0., 1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=3,
            len_right_core=3,
            len_sorted_core=2,
            eph_left_core=0.,
            eph_middle_core=0.0625,
            eph_right_core=0.0625,
            eph_sorted_core=0.375
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 1., 0., 1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=1 / 6,
            eph_right_core=1 / 6,
            eph_sorted_core=1 / 6
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 1., 1., 1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=4,
            len_right_core=4,
            len_sorted_core=4,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 1., 1., 1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=2,
            len_right_core=2,
            len_sorted_core=2,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 1., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=2,
            len_right_core=4,
            len_sorted_core=2,
            eph_left_core=0.375,
            eph_middle_core=0.375,
            eph_right_core=0.,
            eph_sorted_core=0.375
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 1., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=3,
            len_sorted_core=1,
            eph_left_core=1 / 6,
            eph_middle_core=1 / 6,
            eph_right_core=0,
            eph_sorted_core=1 / 6
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=10,
            len_sorted_core=1,
            eph_left_core=0.875,
            eph_middle_core=0.875,
            eph_right_core=0.,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=10,
            len_sorted_core=1,
            eph_left_core=2 / 3,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=5,
            len_middle_core=1,
            len_right_core=6,
            len_sorted_core=1,
            eph_left_core=0.375,
            eph_middle_core=0.875,
            eph_right_core=0.25,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=5,
            len_middle_core=1,
            len_right_core=6,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=3,
            len_middle_core=1,
            len_right_core=8,
            len_sorted_core=1,
            eph_left_core=0.625,
            eph_middle_core=0.875,
            eph_right_core=0.,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=3,
            len_middle_core=1,
            len_right_core=8,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=1,
            len_right_core=7,
            len_sorted_core=1,
            eph_left_core=0.5,
            eph_middle_core=0.875,
            eph_right_core=0.125,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=4,
            len_middle_core=1,
            len_right_core=7,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=8,
            len_middle_core=1,
            len_right_core=3,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.875,
            eph_right_core=0.625,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=8,
            len_middle_core=1,
            len_right_core=3,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=9,
            len_middle_core=1,
            len_right_core=2,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.875,
            eph_right_core=0.75,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=9,
            len_middle_core=1,
            len_right_core=2,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=1 / 3,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=10,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=0.875,
            eph_right_core=0.875,
            eph_sorted_core=0.875
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=10,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=2 / 3,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=[.1, .1, .1, .1, .1, .1, .1, .1, .1, .1],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=8,
            len_middle_core=8,
            len_right_core=8,
            len_sorted_core=8,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[.1, .1, .1, .1, .1, .1, .1, .1, .1, .1],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=3,
            len_middle_core=3,
            len_right_core=3,
            len_sorted_core=3,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., .2, .55, 0., .15, .1, 0., 0.],
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=7,
            len_middle_core=4,
            len_right_core=6,
            len_sorted_core=3,
            eph_left_core=0.125,
            eph_middle_core=0.5,
            eph_right_core=0.25,
            eph_sorted_core=0.625
        )
    ),
    EphemeralityTestCase(
        input_sequence=[0., 0., 0., .2, .55, 0., .15, .1, 0., 0.],
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=5,
            len_middle_core=1,
            len_right_core=6,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2 / 3,
            eph_right_core=0.,
            eph_sorted_core=2 / 3
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.eye(1, 10000, k=5000).flatten(),
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=5001,
            len_middle_core=1,
            len_right_core=5000,
            len_sorted_core=1,
            eph_left_core=0.374875,
            eph_middle_core=0.999875,
            eph_right_core=0.375,
            eph_sorted_core=0.999875
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.eye(1, 10000, k=5000).flatten(),
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=5001,
            len_middle_core=1,
            len_right_core=5000,
            len_sorted_core=1,
            eph_left_core=0.,
            eph_middle_core=2999 / 3000,
            eph_right_core=0.,
            eph_sorted_core=2999 / 3000
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.ones((10000,)),
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=8000,
            len_middle_core=8000,
            len_right_core=8000,
            len_sorted_core=8000,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.ones((10000,)),
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=3000,
            len_middle_core=3000,
            len_right_core=3000,
            len_sorted_core=3000,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.pad(np.zeros((9996,)), pad_width=(2, 2), constant_values=(1., 1.)),
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=10000,
            len_middle_core=10000,
            len_right_core=10000,
            len_sorted_core=4,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=0.9995
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.pad(np.zeros((9996,)), pad_width=(2, 2), constant_values=(1., 1.)),
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=2,
            len_middle_core=9998,
            len_right_core=2,
            len_sorted_core=2,
            eph_left_core=1499 / 1500,
            eph_middle_core=0.,
            eph_right_core=1499 / 1500,
            eph_sorted_core=1499 / 1500
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.pad(np.eye(1, 9999, k=4999).flatten(), pad_width=(1, 1), constant_values=(1., 1.)),
        threshold=0.8,
        expected_output=ResultSet(
            len_left_core=10001,
            len_middle_core=10001,
            len_right_core=10001,
            len_sorted_core=3,
            eph_left_core=0.,
            eph_middle_core=0.,
            eph_right_core=0.,
            eph_sorted_core=39989 / 40004
        )
    ),
    EphemeralityTestCase(
        input_sequence=np.pad(np.eye(1, 9999, k=4999).flatten(), pad_width=(1, 1), constant_values=(1., 1.)),
        threshold=0.3,
        expected_output=ResultSet(
            len_left_core=1,
            len_middle_core=1,
            len_right_core=1,
            len_sorted_core=1,
            eph_left_core=29993 / 30003,
            eph_middle_core=29993 / 30003,
            eph_right_core=29993 / 30003,
            eph_sorted_core=29993 / 30003
        )
    )
]


class TestComputeEphemerality(TestCase):
    def test_compute_ephemeralities(self):
        for i, test_case in enumerate(TEST_CASES):
            with self.subTest():
                print(f'\nRunning test case {i}: {test_case.input_sequence}, threshold {test_case.threshold}...')

                actual_output = compute_ephemerality(frequency_vector=test_case.input_sequence,
                                                     threshold=test_case.threshold)

                try:
                    self.assertEquals(test_case.expected_output, actual_output)
                except AssertionError as ex:
                    print(f"\tAssertion error while processing test case {i}: {test_case.input_sequence}, "
                          f"threshold {test_case.threshold}...")
                    print(f"\t\tExpected output: {test_case.expected_output}\n\t\tActual output: {actual_output}")
                    raise ex

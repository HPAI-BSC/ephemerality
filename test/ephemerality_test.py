import warnings
from unittest import TestCase

from typing import Sequence
import numpy as np
from dataclasses import dataclass
import re

from src import compute_ephemerality


@dataclass
class EphemeralityTestCase:
    input_vector: Sequence[float]
    threshold: float
    expected_output: dict
    warnings: tuple[bool, bool, bool]


class TestComputeEphemerality(TestCase):
    _warning_messages = [
        re.compile(
            r'Original ephemerality value is less than 0 [(]-[0-9]*[.][0-9]*[)] and is going to be rounded up! '
            r'This is indicative of the edge case in which ephemerality span is greater than '
            r'\[threshold [*] input_vector_length], i[.]e[.] most of the frequency mass lies in a few vector '
            r'elements at the end of the frequency vector[.] Original ephemerality in this case should be '
            r'considered to be equal to 0[.] However, please double check the input vector!'
        ),

        re.compile(
            r'Filtered ephemerality value is less than 0 [(]-[0-9]*[.][0-9]*[)] and is going to be rounded up! '
            r'This is indicative of the edge case in which ephemerality span is greater than '
            r'\[threshold [*] input_vector_length], i[.]e[.] most of the frequency mass lies in a few elements '
            r'at the beginning and the end of the frequency vector[.] Filtered ephemerality in this case should '
            r'be considered to be equal to 0[.] However, please double check the input vector!'
        ),

        re.compile(
            r'Sorted ephemerality value is less than 0 [(]-[0-9]*[.][0-9]*[)] and is going to be rounded up! '
            r'This is indicative of the rare edge case of very short and mostly uniform frequency vector [(]so '
            r'that ephemerality span is greater than \[threshold [*] input_vector_length][)][.] '
            r'Sorted ephemerality in this case should be considered to be equal to 0[.] '
            r'However, please double check the input vector!'
        )
    ]

    _test_cases = [
        EphemeralityTestCase(
            input_vector=[1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.375, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0.375, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.375, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[0., 1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0.375, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.375, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[.5, .5],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 2,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 2
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[.5, .5],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[0.7, .3],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 2,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 2
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[0.7, .3],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 1
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.6875, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0.6875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.6875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 1 / 6, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 1 / 6, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 1 / 6, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 4,
                'ephemerality_filtered': 0.6875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.6875, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 4,
                'ephemerality_filtered': 1 / 6, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 1 / 6, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 1., 0., 1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 4,
                'ephemerality_filtered': 0.0625, 'ephemerality_filtered_span': 3,
                'ephemerality_sorted': 0.375, 'ephemerality_sorted_span': 2
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 1., 0., 1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 1 / 6, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 1 / 6, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 1., 1., 1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 4,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 4,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 4
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[1., 1., 1., 1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 2,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 2
            },
            warnings=(True, True, True)
        ),
        EphemeralityTestCase(
            input_vector=[1., 1., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.375, 'ephemerality_original_span': 2,
                'ephemerality_filtered': 0.375, 'ephemerality_filtered_span': 2,
                'ephemerality_sorted': 0.375, 'ephemerality_sorted_span': 2
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 1., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 1 / 6, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 1 / 6, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 1 / 6, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.875, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 2 / 3, 'ephemerality_original_span': 1,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.375, 'ephemerality_original_span': 5,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 5,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.625, 'ephemerality_original_span': 3,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 3,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.5, 'ephemerality_original_span': 4,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 4,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 8,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 8,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 9,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 0., 1., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 9,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 10,
                'ephemerality_filtered': 0.875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.875, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 10,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[.1, .1, .1, .1, .1, .1, .1, .1, .1, .1],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 8,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 8,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 8
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[.1, .1, .1, .1, .1, .1, .1, .1, .1, .1],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 3,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 3,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 3
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., .2, .55, 0., .15, .1, 0., 0.],
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.125, 'ephemerality_original_span': 7,
                'ephemerality_filtered': 0.5, 'ephemerality_filtered_span': 4,
                'ephemerality_sorted': 0.625, 'ephemerality_sorted_span': 3
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=[0., 0., 0., .2, .55, 0., .15, .1, 0., 0.],
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 5,
                'ephemerality_filtered': 2 / 3, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2 / 3, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=np.eye(1, 10000, k=5000).flatten(),
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0.375, 'ephemerality_original_span': 5000,
                'ephemerality_filtered': 0.999875, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 0.999875, 'ephemerality_sorted_span': 1
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=np.eye(1, 10000, k=5000).flatten(),
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 5000,
                'ephemerality_filtered': 2999 / 3000, 'ephemerality_filtered_span': 1,
                'ephemerality_sorted': 2999 / 3000, 'ephemerality_sorted_span': 1
            },
            warnings=(True, False, False)
        ),
        EphemeralityTestCase(
            input_vector=np.ones((10000,)),
            threshold=0.8,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 8000,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 8000,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 8000
            },
            warnings=(False, False, False)
        ),
        EphemeralityTestCase(
            input_vector=np.ones((10000,)),
            threshold=0.3,
            expected_output={
                'ephemerality_original': 0., 'ephemerality_original_span': 3000,
                'ephemerality_filtered': 0., 'ephemerality_filtered_span': 3000,
                'ephemerality_sorted': 0., 'ephemerality_sorted_span': 3000
            },
            warnings=(False, False, False)
        )
    ]

    def add_test_case(self,
                      input_vector: Sequence[float],
                      threshold: float,
                      expected_output: dict,
                      warnings: tuple[bool, bool, bool]):
        self._test_cases.append(EphemeralityTestCase(
            input_vector=input_vector,
            threshold=threshold,
            expected_output=expected_output,
            warnings=warnings
        ))

    def clear(self):
        self._test_cases = list()

    @staticmethod
    def round_ephemeralities(ephemeralities: dict, precision: int=8):
        np.round_(ephemeralities['ephemerality_original'], precision)
        np.round_(ephemeralities['ephemerality_filtered'], precision)
        np.round_(ephemeralities['ephemerality_sorted'], precision)

    def test_compute_ephemeralities(self):
        for i, test_case in enumerate(self._test_cases):
            print(f'\nRunning test case {i}: {test_case.input_vector}, threshold {test_case.threshold}...')
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always', category=RuntimeWarning)

                actual_output = compute_ephemerality(frequency_vector=test_case.input_vector,
                                                     threshold=test_case.threshold)

                self.assertEqual(self.round_ephemeralities(test_case.expected_output),
                                 self.round_ephemeralities(actual_output))

                warn_messages = ""
                for warn in warns:
                    warn_messages += str(warn.message)

                actual_warnings = tuple((TestComputeEphemerality._warning_messages[i].search(warn_messages) is not None
                                         for i in range(3)))

                self.assertEqual(test_case.warnings, actual_warnings)

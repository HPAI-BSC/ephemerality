from typing import Sequence
from dataclasses import dataclass

from ephemerality import EphemeralitySet


@dataclass
class EphemeralityTestCase:
    input_sequence: Sequence[float]
    threshold: float
    expected_output: EphemeralitySet

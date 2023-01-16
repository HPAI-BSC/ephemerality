from typing import Sequence
from src import compute_ephemerality, EphemeralitySet


def get_all_ephemeralities(input_vector: Sequence[float], threshold: float) -> EphemeralitySet:
    return compute_ephemerality(frequency_vector=input_vector, threshold=threshold, types='all')

def get_left_core_ephemerality(input_vector: Sequence[float], threshold: float) -> EphemeralitySet:
    return compute_ephemerality(frequency_vector=input_vector, threshold=threshold, types='left')

def get_middle_core_ephemerality(input_vector: Sequence[float], threshold: float) -> EphemeralitySet:
    return compute_ephemerality(frequency_vector=input_vector, threshold=threshold, types='middle')

def get_right_core_ephemerality(input_vector: Sequence[float], threshold: float) -> EphemeralitySet:
    return compute_ephemerality(frequency_vector=input_vector, threshold=threshold, types='right')

def get_sorted_core_ephemerality(input_vector: Sequence[float], threshold: float) -> EphemeralitySet:
    return compute_ephemerality(frequency_vector=input_vector, threshold=threshold, types='sorted')
import json
import os

import numpy as np


def generate_test_case(size: int, seed: None | int=None) -> tuple[float, list[float]]:
    vector = np.zeros((size,))
    rng = np.random.default_rng(seed)
    threshold = rng.uniform(low=0.1, high=0.9, size=None)
    vector[0] = rng.normal(scale=10)
    for i in range(1, size):
        vector[i] = vector[i-1] + rng.normal()
    vector -= np.mean(vector)
    vector = vector.clip(min=0)
    vector /= np.sum(vector)

    return threshold, list(vector)


def generate_data(max_size: int=10, inputs_per_n: int=100, seed: int=2023, save_dir: str= "./test_data/") -> None:
    if save_dir and save_dir[-1] != '/':
        save_dir += '/'

    for n in range(1, max_size):
        dir_n = f"{save_dir}{n}"
        os.makedirs(dir_n, exist_ok=True)

        for i in range(inputs_per_n):
            test_case = generate_test_case(10**n, seed + i)
            test_data = [{
                "threshold": test_case[0],
                "input_sequence": test_case[1]
            }]

            with open(f"{dir_n}/{i}.json", "w") as f:
                json.dump(test_data, f)

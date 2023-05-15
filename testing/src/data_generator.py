import json
import os
import numpy as np
from pathlib import Path
import shutil
from datetime import datetime


def generate_test_case(
        size: int,
        data_type: str,
        data_range: tuple[float, float] | None = None,
        seed: None | int = None,
        activity_length: None | int = None
) -> tuple[float, list[float | str]]:

    if activity_length is None:
        activity_length = size
    activity = np.zeros((activity_length,))
    rng = np.random.default_rng(seed)
    threshold = float(rng.uniform(low=0.1, high=0.9, size=None))
    activity[0] = rng.normal(scale=10)
    for i in range(1, activity_length):
        activity[i] = activity[i - 1] + rng.normal()
    activity -= np.mean(activity)
    activity = activity.clip(min=0)

    if data_type == "activity" or data_type == "a":
        activity /= np.sum(activity)
        return threshold, list(activity)

    activity_granule_length = int(np.ceil((data_range[1] - data_range[0]) / activity_length))
    activity = activity.repeat(activity_granule_length)[:(data_range[1] - data_range[0])]
    activity /= np.sum(activity)

    timestamps = rng.choice(
        a=np.arange(data_range[0], data_range[1]).astype(int),
        size=size,
        p=activity
    )
    timestamps.sort()

    if data_type == "timestamps" or data_type == "t":
        return threshold, list(timestamps.astype(str))

    return threshold, [datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S.%fZ").replace("000000Z", "000Z")
                       for ts in timestamps]


def generate_data(
        max_size: int = 10,
        inputs_per_n: int = 100,
        data_type: str = "a",
        data_range: tuple[float, float] | None = None,
        seed: int = 2023,
        save_dir: str = "./test_data/"
) -> None:
    if save_dir and save_dir[-1] != '/':
        save_dir += '/'

    for n in range(1, max_size + 1):
        dir_n = Path(f"{save_dir}{n}")
        dir_n.mkdir(parents=True, exist_ok=True)

        for i in range(inputs_per_n):
            size = 10 ** n
            test_case = generate_test_case(
                size=size,
                data_type=data_type,
                data_range=data_range,
                seed=seed + i,
                activity_length=None if data_type == "activity" or data_type == "a" else int((data_range[1] - data_range[0]) / 1000)
            )
            test_data = [{
                "threshold": test_case[0],
                "input_sequence": test_case[1],
                "input_type": data_type,
                "range": [str(data_range[0]), str(data_range[1])],
                "reference_name": f"{data_type}_{size}_{i}"
            }]

            with open(f"{dir_n}/{i}.json", "w") as f:
                json.dump(test_data, f)


def clear_data(folder: str) -> None:
    for file in Path(folder).iterdir():
        try:
            if file.is_file() or file.is_symlink():
                file.unlink()
            elif file.is_dir():
                shutil.rmtree(file)
        except Exception as ex:
            print(f'Failed to delete {file.resolve()}. Reason: {ex}')

import json
import sys
from pathlib import Path
from subprocess import check_output

import requests


def test_performance(
        input_folder: str,
        url: str | None,
        types: str,
        tests_per_case: int
) -> dict[str, dict[str, list]]:
    results = {}
    if url:
        if url[-1] != '/':
            url += '/'
        if 't' in types:
            time_results = {}
            for json_file in Path(input_folder).rglob("*.json"):
                with open(json_file, 'r') as f:
                    test_case = json.load(f)
                case_times = []
                for i in range(tests_per_case):
                    response = requests.post(f"{url}?test_time_reps={1}", json=test_case)
                    case_times.append(response.json()["time"][0])
                time_results[str(json_file.resolve())] = case_times
            results["time"] = time_results
        if 'r' in types:
            ram_results = {}
            for json_file in Path(input_folder).rglob("*.json"):
                with open(json_file, 'r') as f:
                    test_case = json.load(f)
                case_rams = []
                for i in range(tests_per_case):
                    response = requests.post(f"{url}?test_ram_reps={1}", json=test_case)
                    case_rams.append(response.json()["RAM"][0])
                ram_results[str(json_file.resolve())] = case_rams
            results["RAM"] = ram_results
    else:
        if 't' in types:
            time_results = {}
            for json_file in Path(input_folder).rglob("*.json"):
                print(json_file.resolve())
                case_times = []
                for i in range(tests_per_case):
                    run_results = check_output([
                        "python3", "-m", "ephemerality", "cmd",
                        "-i", str(json_file.resolve()),
                        "--test_time_reps", "1"
                    ]).decode(sys.stdout.encoding)
                    run_results = json.loads(run_results)["time"]
                    case_times.append(run_results[list(run_results.keys())[0]][0])
                time_results[str(json_file.resolve())] = case_times
            results["time"] = time_results
        if 'r' in types:
            ram_results = {}
            for json_file in Path(input_folder).rglob("*.json"):
                print(json_file.resolve())
                case_rams = []
                for i in range(tests_per_case):
                    run_results = check_output([
                        "python", "ephemerality_cmd.py",
                        "-i", str(json_file.resolve()),
                        "--test_ram_reps", "1"
                    ]).decode(sys.stdout.encoding)
                    run_results = json.loads(run_results)["RAM"]
                    case_rams.append(run_results[list(run_results.keys())[0]][0])
                ram_results[str(json_file.resolve())] = case_rams
            results["RAM"] = ram_results

    return results

import json

from _version import __version__
import argparse
import os
from subprocess import check_output
import shutil
import requests
from pathlib import Path

from testing import generate_data


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [TYPE(s)] [-h] [-v] [-u URL] [-i INPUT_FOLDER] [-r TESTS_PER_CASE] [-g] [-n MAX_TEST_SIZE] "
              "[-m CASES_PER_BATCH] [-s SEED] [-k]...",
        description="Run performance tests."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version {__version__}"
    )
    parser.add_argument(
        "-u", "--url", action="store", default="",
        help="URL of REST web service. If not provided, will run tests on command line script instead."
    )
    parser.add_argument(
        "-i", "--input_folder", action="store", default="./test_data/",
        help="Path to the folder with test cases. It will be created if it doesn't exist. "
             "Will create a \"performance.json\" file for each subfolder (including the root folder) with input files. "
             "Defaults to \"./test_data/\"."
    )
    parser.add_argument(
        "-r", "--tests_per_case", action="store", type=int, default=20,
        help="Number of test repetitions per test case per test. Defaults to 20."
    )
    parser.add_argument(
        "-g", "--generate", action="store_true",
        help="Generate test cases using numpy random number generator. Will generate N batches of inputs. Each one "
             "will contain M JSON files with thresholds and input vectors, "
             "each vector is of length 10^[batch number from 1 to N]. "
             "WARNING: will rewrite the contents of the input folder."
    )
    parser.add_argument(
        "-n", "--max_size", action="store", type=int, default=6,
        help="Maximal size (in power 10) of test size batches. Defaults to 6."
    )
    parser.add_argument(
        "-m", "--cases_per_batch", action="store", type=int, default=20,
        help="Number of test cases in each size batch. Defaults to 20."
    )
    parser.add_argument(
        "-s", "--seed", action="store", type=int, default=2023,
        help="Value of the seed to be used for test case generation. Defaults to 2023."
    )
    parser.add_argument(
        "-k", "--keep_data", action="store_true",
        help="Keep generated test data after tests finish. All GENERATED data will be removed otherwise."
    )
    parser.add_argument(
        'types', action="store", default="tcr",
        help='test types: \"t\" for computation time, \"r\" for RAM usage. Defaults to \"tr\"'
    )
    return parser



if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    if args.tests_per_case <= 0:
        raise ValueError("\"tests_per_case\" value should be positive!")
    if args.max_size <= 0:
        raise ValueError("\"max_size\" value should be positive!")
    if args.cases_per_batch <= 0:
        raise ValueError("\"cases_per_batch\" value should be positive!")

    # Data
    if args.generate:
        generate_data(
            max_size=args.max_size,
            inputs_per_n=args.cases_per_batch,
            seed=args.seed,
            save_dir=args.input_folder)
    else:
        if not os.path.exists(args.input_folder):
            raise FileNotFoundError("Input folder does not exist and no data generation has been requested!")
        elif not os.path.isdir(args.input_folder):
            raise NotADirectoryError("Specified input folder is not a directory.")



    # Test

    results = {}
    if args.url:
        if args.url[-1] != '/':
            args.url += '/'
        if 't' in args.types:
            time_results = {}
            for json_file in Path(args.input_folder).rglob("*.json"):
                with open(json_file, 'r') as f:
                    test_case = json.load(f)
                case_times = []
                for i in range(args.tests_per_case):
                    response = requests.post(f"args.url?test_time_reps={1}", json=test_case)
                    case_times.append(response.json()["time"][0])
                time_results[str(json_file.absolute())] = case_times
            results["time"] = time_results
        if 'r' in args.types:
            ram_results = {}
            for json_file in Path(args.input_folder).rglob("*.json"):
                with open(json_file, 'r') as f:
                    test_case = json.load(f)
                case_rams = []
                for i in range(args.tests_per_case):
                    response = requests.post(f"{args.url}?test_ram_reps={1}", json=test_case)
                    case_rams.append(response.json()["RAM"][0])
                ram_results[str(json_file.absolute())] = case_rams
            results["RAM"] = ram_results
    else:
        if 't' in args.types:
            time_results = {}
            for json_file in Path(args.input_folder).rglob("*.json"):
                case_times = []
                for i in range(args.tests_per_case):
                    run_results = check_output([
                        "python", "ephemerality-cmd.py",
                        "-i", str(json_file.absolute()),
                        "--test_time_reps", "1"
                    ])
                    case_times.append(json.load(run_results)["time"][0])
                time_results[str(json_file.absolute())] = case_times
            results["time"] = time_results
        if 'r' in args.types:
            ram_results = {}
            for json_file in Path(args.input_folder).rglob("*.json"):
                case_rams = []
                for i in range(args.tests_per_case):
                    run_results = check_output([
                        "python", "ephemerality-cmd.py",
                        "-i", str(json_file.absolute()),
                        "--test_ram_reps", "1"
                    ])
                    case_rams.append(json.load(run_results)["RAM"][0])
                ram_results[str(json_file.absolute())] = case_rams
            results["RAM"] = ram_results

    print(results)

    with open('./test_results.json', 'w+') as f:
        json.dump(results, f)

    if args.generate and not args.keep_data:
        for filename in os.listdir(args.input_folder):
            file_path = os.path.join(args.input_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

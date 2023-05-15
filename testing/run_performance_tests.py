#!/usr/bin/env python3

import json
from argparse import ArgumentParser
import os
from pathlib import Path
from pprint import pprint

from testing import generate_data, clear_data
from testing.src import test_performance


def init_parser() -> ArgumentParser:
    parser = ArgumentParser(
        usage="python3 %(prog)s [TYPE(s)] [-h] [-u URL] [-i INPUT_FOLDER] [-o OUTPUT_FILE] [--merge_output] "
              "[-r TESTS_PER_CASE] [-g] [-d DATA_TYPE] [--data_range START END] [-n MAX_TEST_SIZE] "
              "[-m CASES_PER_BATCH] [-s SEED] [-k] ...",
        description="Run performance tests."
    )
    parser.add_argument(
        "-u", "--url", action="store", default="",
        help="URL of REST web service. If not provided, will run tests on command line script instead."
    )
    parser.add_argument(
        "-i", "--input_folder", action="store", default="./test_data/",
        help="Path to the folder with test cases. It will be created if it doesn't exist. "
             "Defaults to \"./test_data/\"."
    )
    parser.add_argument(
        "-o", "--output_file", action="store", default="./test_results.json",
        help="Name and path to the JSON file to which the test results will be written. The path will be created if needed. "
             "Defaults to \"./test_results.json\"."
    )
    parser.add_argument(
        "--merge_output", action="store_true",
        help="Merges the output of the test with the existing content of the file in top-level array. By default the "
             "file is overwritten."
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
        "-d", "--data_type", action="store", choices=["activity", "a", "timestamps", "t", "datetime", "d"], default="a",
        help="Type of the generated data. Defaults to \"a\"."
    )
    parser.add_argument(
        "--data_range", action="store", type=float, nargs=2, default=None,
        help="Value range for timestamps or datetime data types in UNIX timestamp in seconds. "
             "Passed as 2 integer numbers. Defaults to (0, 31536000)."
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
        'types', action="store", default="tr", nargs='?',
        help='test types: \"t\" for computation time, \"r\" for RAM usage. Defaults to \"tr\"'
    )
    return parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    if args.data_range is None:
        args.data_range = (0, 31536000)

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
            data_type=args.data_type,
            data_range=args.data_range,
            seed=args.seed,
            save_dir=args.input_folder)
    else:
        if not os.path.exists(args.input_folder):
            raise FileNotFoundError("Input folder does not exist and no data generation has been requested!")
        elif not os.path.isdir(args.input_folder):
            raise NotADirectoryError("Specified input folder is not a directory.")

    # Test
    results = test_performance(
        input_folder=args.input_folder,
        url=args.url,
        types=args.types,
        tests_per_case=args.tests_per_case
    )
    pprint(results)

    # Save results
    if args.output_file:
        output_file = Path(args.output_file).resolve()
        if not output_file.exists():
            if not output_file.parent.exists():
                output_file.parent.mkdir(parents=True)
            mode = "w"
        else:
            mode = "w+" if args.merge_output else "w"

        with open(output_file, mode) as f:
            if mode == "w":
                json.dump(results, f, indent=2, sort_keys=True)
            else:
                previous_output = json.load(f)
                if isinstance(previous_output, list):
                    previous_output.append(results)
                    json.dump(previous_output, f)
                else:
                    json.dump([previous_output, results], f)

    # Clear data
    if args.generate and not args.keep_data:
        clear_data(args.input_folder)

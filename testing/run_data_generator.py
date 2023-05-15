#!/usr/bin/env python3

from argparse import ArgumentParser

from testing import generate_data


def init_parser() -> ArgumentParser:
    parser = ArgumentParser(
        usage="python3 %(prog)s [-o OUTPUT_FOLDER][-g] [-d DATA_TYPE] [--data_range START END] "
              "[-n MAX_TEST_SIZE] [-m CASES_PER_BATCH] [-s SEED] ...",
        description="Generate data for tests."
    )
    parser.add_argument(
        "-o", "--output_folder", action="store", default="./test_data/",
        help="Path to the folder to store generated test cases. Defaults to \"./test_data/\"."
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
    return parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    if args.data_range is None:
        args.data_range = (0, 31536000)

    if args.max_size <= 0:
        raise ValueError("\"max_size\" value should be positive!")
    if args.cases_per_batch <= 0:
        raise ValueError("\"cases_per_batch\" value should be positive!")

    generate_data(
        max_size=args.max_size,
        inputs_per_n=args.cases_per_batch,
        data_type=args.data_type,
        data_range=args.data_range,
        seed=args.seed,
        save_dir=args.output_folder)

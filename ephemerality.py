from _version import __version__
import sys
import json
import argparse
import numpy as np
from src import compute_ephemerality


HELP_INFO = ""


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [FREQUENCY_VECTOR] [-h] [-v] [-i INPUT_FILE] [-o OUTPUT_FILE.json] [-t THRESHOLD]...",
        description="Calculate ephemerality for a given vector of frequencies."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version {__version__}"
    )
    parser.add_argument(
        "-p", "--print", action="store_true",
        help="If output file is provided, forces the results to still be printed to stdout."
    )
    parser.add_argument(
        "-i", "--input", action="store",
        help="Path to the input csv file. If not specified, will use the command line arguments "
             "(delimited either by commas or spaces)."
    )
    parser.add_argument(
        "-o", "--output", action="store",
        help="Path to the output json file. If not specified, will output ephemerality values to stdout in the"
             " following format separated by a space: \"EPH_ORIG EPH_ORIG_SPAN EPH_FILT EPH_FILT_SPAN EPH_SORT "
             "EPH_SORT_SPAN\""
    )
    parser.add_argument(
        "-t", "--threshold", action="store", default=0.8,
        help="Threshold value for ephemerality computations. Defaults to 0.8."
    )
    parser.add_argument(
        'frequencies',
        help='frequency vector (if the input file is not specified)',
        nargs='*'
    )
    return parser


def print_ephemeralities(ephemerality_list: list[dict]):
    for ephemeralities in ephemerality_list:
        print(f"{ephemeralities['ephemerality_original']} {ephemeralities['ephemerality_original_span']} "
              f"{ephemeralities['ephemerality_filtered']} {ephemeralities['ephemerality_filtered_span']} "
              f"{ephemeralities['ephemerality_sorted']} {ephemeralities['ephemerality_sorted_span']}")


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    frequency_vectors = list()

    if args.input:
        with open(args.input, 'r') as f:
            for line in f.readlines():
                if line.strip():
                    frequency_vectors.append(np.array(line.split(','), dtype=float))
    else:
        if len(args.frequencies) > 1:
            frequency_vectors.append(np.array(args.frequencies, dtype=float))
        elif len(args.frequencies) == 1:
            if ' ' in args.frequencies[0]:
                frequency_vectors.append(np.array(args.frequencies[0].split(' '), dtype=float))
            else:
                frequency_vectors.append(np.array(args.frequencies[0].split(','), dtype=float))
        else:
            sys.exit('No input provided!')

    threshold = float(args.threshold)

    ephemerality_list = list()
    for frequency_vector in frequency_vectors:
        ephemerality_list.append(compute_ephemerality(frequency_vector=frequency_vector, threshold=threshold).dict())

    if args.output:
        with open(args.output, 'w+') as f:
            json.dump(ephemerality_list, f, indent=2)
        if args.print:
            print_ephemeralities(ephemerality_list)
    else:
        print_ephemeralities(ephemerality_list)

import json
import sys
import time
from argparse import ArgumentParser, Namespace, SUPPRESS
from pathlib import Path
from memory_profiler import memory_usage

import numpy as np
from ephemerality.src import compute_ephemerality, process_input, ProcessedData


def init_cmd_parser(parser: ArgumentParser) -> ArgumentParser:
    parser.usage = "%(prog)s [activity] [-h] [-i INPUT_FILE] [-r] [-o OUTPUT_FILE.json] [-t THRESHOLD]..."
    parser.description = "Calculate ephemerality for a given activity vector or a set of timestamps."
    parser.add_argument(
        "-p", "--print", action="store_true",
        help="If an output file is specified, forces the results to still be printed to stdout."
    )
    parser.add_argument(
        "-i", "--input", action="store",
        help="Path to either a JSON or CSV file with input data, or to the folder with files. If not specified, "
             "will read the activity vector from the command line (as numbers delimited by either commas or spaces)."
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Used with a folder-type input to specify to also process files in the full subfolder tree. "
             "Defaults to False."
    )
    parser.add_argument(
        "-o", "--output", action="store",
        help="Path to an output JSON file. If not specified, will output ephemerality values to stdout in JSON format."
    )
    parser.add_argument(
        "--output_indent", action="store", type=int, default=-1,
        help="Sets the indentation level of the output (either a JSON file or STDOUT) in terms of number of spaces per "
             "level. If negative, will output results as a single line. Defaults to -1."
    )
    parser.add_argument(
        "-t", "--threshold", action="store", type=float, default=0.8,
        help="Threshold value for ephemerality computations in case of CSV input. Defaults to 0.8."
    )
    parser.add_argument(
        "--test_time_reps", action="store", type=int, default=0,
        help=SUPPRESS
    )
    parser.add_argument(
        "--test_ram_reps", action="store", type=int, default=0,
        help=SUPPRESS
    )
    parser.add_argument(
        'activity', type=float,
        help='Activity vector (if the input file is not specified)',
        nargs='*'
    )
    parser.set_defaults(
        func=exec_cmd_compute_call
    )
    return parser


def exec_cmd_compute_call(input_args: Namespace) -> None:
    if input_args.input:
        path = Path(input_args.input)
        if path.is_dir():
            input_cases = process_input(input_folder=input_args.input, recursive=input_args.recursive)
        elif path.is_file():
            input_cases = process_input(input_file=input_args.input, threshold=float(input_args.threshold))
        else:
            raise ValueError("Unknown input file format!")
    else:
        input_cases: list[ProcessedData] = []
        if len(input_args.activity) > 1:
            input_cases.append(
                ProcessedData(
                    name="cmd-input",
                    activity=np.array(input_args.activity, dtype=float),
                    threshold=float(input_args.threshold)))
        elif len(input_args.activity) == 1:
            if ' ' in input_args.activity[0]:
                input_cases.append(
                    ProcessedData(
                        name="cmd-input",
                        activity=np.array(input_args.activity[0].split(' '), dtype=float),
                        threshold=float(input_args.threshold)))
            else:
                input_cases.append(
                    ProcessedData(
                        name="cmd-input",
                        activity=np.array(input_args.activity[0].split(','), dtype=float),
                        threshold=float(input_args.threshold)))
        else:
            sys.exit('No input provided!')

    results = {}

    if input_args.test_time_reps > 0 or input_args.test_ram_reps > 0:
        if input_args.test_time_reps:
            for input_case in input_cases:
                results["time"] = dict()
                times = []
                for i in range(input_args.test_time_reps):
                    start_time = time.time()
                    compute_ephemerality(activity_vector=input_case.activity, threshold=input_case.threshold).dict()
                    times.append(time.time() - start_time)
                results["time"][input_case.name] = times
        if input_args.test_ram_reps:
            for input_case in input_cases:
                results["RAM"] = dict()
                rams = []
                for i in range(input_args.test_ram_reps):
                    rams.append(memory_usage(
                        (compute_ephemerality, [], {"activity_vector": input_case.activity, "threshold": input_case.threshold}),
                        max_usage=True
                    ))
                results["RAM"][input_case.name] = rams
    else:
        for input_case in input_cases:
            results[input_case.name] = compute_ephemerality(activity_vector=input_case.activity,
                                                            threshold=input_case.threshold).dict()

    output_indent = input_args.output_indent if input_args.output_indent >= 0 else None
    if input_args.output:
        with open(input_args.output, 'w') as f:
            json.dump(results, f, indent=output_indent, sort_keys=True)
        if input_args.print:
            print(json.dumps(results, indent=output_indent, sort_keys=True))
        else:
            return None
    else:
        print(json.dumps(results, indent=output_indent, sort_keys=True))

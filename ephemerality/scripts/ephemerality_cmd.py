from argparse import ArgumentParser, Namespace, SUPPRESS
import json
import sys
from pathlib import Path

import numpy as np

from ephemerality import compute_ephemerality, process_input, ProcessedData


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
    for input_case in input_cases:
        results[input_case.name] = (compute_ephemerality(activity_vector=input_case.activity,
                                                         threshold=input_case.threshold).dict())

    if input_args.output:
        with open(input_args.output, 'w+') as f:
            json.dump(results, f, indent=2)
        if input_args.print:
            print(json.dumps(results, indent=2))
        else:
            return None
    else:
        print(json.dumps(results, indent=2))


# if __name__ == '__main__':
#     parser = init_cmd_argparse()
#     args = parser.parse_args()
#
#     if args.test_time_reps == 0 and args.test_ram_reps == 0:
#         output = run(input_args=args)
#         if output:
#             print(output)
#     else:
#         output = {}
#         if args.test_time_reps > 0:
#             times = []
#             for i in range(args.test_time_reps):
#                 start_time = time.time()
#                 run(input_args=args, supress_save_output=True)
#                 times.append(time.time() - start_time)
#             output["time"] = times
#         if args.test_ram_reps > 0:
#             rams = []
#             for i in range(args.test_ram_reps):
#                 rams.append(memory_usage(
#                     (run, [], {"input_args": args, "supress_save_output": True}),
#                     max_usage=True
#                 )[0])
#             output["RAM"] = rams
#         if args.output:
#             with open(args.output, 'w+') as f:
#                 json.dump(output, f, indent=2)
#             if args.print:
#                 print(json.dumps(output, indent=2))
#         else:
#             print(json.dumps(output, indent=2))

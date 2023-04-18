from argparse import ArgumentParser, Namespace
from subprocess import call

from ephemerality.rest import set_test_mode


def init_api_argparse(parser: ArgumentParser) -> ArgumentParser:
    parser.usage = "%(prog)s [-h] [--host HOST] [--port PORT] [--test] ..."
    parser.description = "Start a REST web service to compute ephemerality computations on requests."
    parser.add_argument(
        "--host", action="store", default="127.0.0.1",
        help="Bind socket to this host. Defaults to \"127.0.0.1\"."
    )
    parser.add_argument(
        "--port", action="store", type=int, default=8080,
        help="Bind to a socket with this port. Defaults to 8080."
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run the web service in a mode that allows to process requests to evaluate time and RAM performance of "
             "the module (can be computationally expensive!)."
    )
    parser.set_defaults(
        func=exec_start_service_call
    )
    return parser


def start_service(host: str = "127.0.0.1", port: int = 8080, test_mode: bool = False) -> None:
    set_test_mode(test_mode)
    call(['uvicorn', 'ephemerality.rest.runner:app', '--host', host, '--port', str(port)])


def exec_start_service_call(input_args: Namespace) -> None:
    start_service(host=input_args.host, port=input_args.port, test_mode=input_args.test)

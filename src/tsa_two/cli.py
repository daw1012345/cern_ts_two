#!/usr/bin/env python3
from argparse import ArgumentParser
from json import JSONDecodeError
from typing import IO, Optional, Sequence

from tsa_two.dependency_resolver.exceptions import (
    DependencyCycleError,
    DependencyJSONError,
    DependencyNotDefinedError,
)
from tsa_two.dependency_resolver.formatters import make_space_formatter, tab_format
from tsa_two.dependency_resolver.resolver import resolve_file


def main(args: Optional[Sequence[str]] = None, file: Optional[IO[str]] = None):
    """The function action as the main CLI entrypoint

    Arguments:
        args (Optional[Sequence[str]]): Arguments to pass to the argument parser (used for testing)
        file (Optional[IO[str]]): File to use instead of STDOUT (used for testing)
    """
    parser = ArgumentParser(prog="tsa_two-cli", description="")
    parser.add_argument("path")

    formatter_group = parser.add_mutually_exclusive_group()
    formatter_group.add_argument(
        "--tabs", action="store_true", help="Enable the tab formatter"
    )
    formatter_group.add_argument(
        "--spaces",
        type=int,
        required=False,
        default=-1,
        help="Enable the space formatter with X spaces / indent",
    )

    args = parser.parse_args(args=args)

    formatter = tab_format

    if args.spaces >= 0:
        formatter = make_space_formatter(args.spaces)

    try:
        res = resolve_file(args.path, formatter)
        print(res, file=file)
    except FileNotFoundError:
        print("Error: Could not find given file", file=file)
    except DependencyCycleError:
        print("Error: Dependency cycle detected. Refusing to continue", file=file)
    except DependencyNotDefinedError:
        print("Error: Dependency referenced but not defined", file=file)
    except DependencyJSONError:
        print("Error: Incorrect JSON format (likely wrong types)", file=file)
    except JSONDecodeError as e:
        print("Error: JSON file could not be parsed", file=file)
        print(e.msg, file=file)


if __name__ == "__main__":
    main()

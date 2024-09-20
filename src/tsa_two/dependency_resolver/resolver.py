#!/usr/bin/env python3
import json
import os
from typing import IO, Callable, List, Mapping

from tsa_two.dependency_resolver.exceptions import (
    DependencyCycleError,
    DependencyJSONError,
    DependencyNotDefinedError,
)
from tsa_two.dependency_resolver.formatters import tab_format


def parse_json(data_src: IO) -> Mapping[str, List[str]]:
    """Takes any `readable` object, reads data and parses any valid
      JSON dependency specification into a dictionary representation

    Arguments:
        data_src (IO): `readable` data source

    Returns:
        Mapping[str, List[str]]
    """
    ret = {}

    raw_json_dict = json.load(data_src)

    # JSON file can have a dict or list as a top-level element
    # We only expect a dict based on the exercise specifications
    if not isinstance(raw_json_dict, dict):
        raise DependencyJSONError("Got a list as top-level element (expected dict!)")

    for package_name, deps in raw_json_dict.items():
        # JSON does not allow for non-str keys
        # Hence, no check for type of package_name

        # JSON can contain lists of objects (invalid for us)
        # Dependencies can be a dict/str instead of a list of strs (which we expect)
        # If this is the case, raise an exception

        if not isinstance(deps, list):
            raise DependencyJSONError("Dependencies are not a list!")

        # As we cannot reasonably parse an object into a string, raise an exception
        if not all(isinstance(e, str) or isinstance(e, int) for e in deps):
            raise DependencyJSONError(
                f"A dependency for {package_name} is not a str or int!"
            )

        # Convert to str to allow for package names that are ints
        ret[package_name] = [str(e) for e in deps]

    return ret


def _format_json(
    inpt: Mapping[str, List[str]], start: str, formatter: Callable[[int, str], str]
) -> str:
    """Internal formatting function. Wraps a nested function which uses a
     recursive DFS-like algorithm to traverse the dependency graph.

    Arguments:
        inpt (Mapping[str, List[str]]): The input dictionary
        start (str): The package to start traversal from
        formatter (Callable[[int, str], str]): fn(indentation, current_dep) -> formatted_string.
         See docstring of `resolve_file` for more information

    Returns:
        str: The formatted dependency graph
    """

    def _do_recursive_format_json(current: str, indent: int, visited: set) -> str:
        # Based on the problem specification, cycles are possible.
        # Here, we assume that such a package/dependency specification is invalid and abort

        if current in visited:
            raise DependencyCycleError(f"Revisited {current}")

        if current not in inpt:
            raise DependencyNotDefinedError(
                f"{current} was declared as a dependency, but is not defined"
            )

        output = formatter(indent, current)
        for dep in inpt.get(current):
            output += _do_recursive_format_json(
                dep, indent + 1, visited | set([current])
            )

        return output

    return _do_recursive_format_json(start, 0, set())


def format_dependency_graph(
    inpt: Mapping[str, List[str]], formatter: Callable[[int, str], str] = tab_format
) -> str:
    """Takes a dictionary (package_name -> [dependencies]) and returns a string formatted using the formatter

    Arguments:
        inpt (Mapping[str, List[str]]): The input dictionary
        formatter (Callable[[int, str], str]): fn(indentation, current_dep) -> formatted_string.
         See docstring of `resolve_file` for more information

    Returns:
        str: formatted dependency graph
    """

    # Go through each package, and format the dependencies of each
    output = ""
    for package in inpt.keys():
        output += _format_json(inpt, package, formatter)

    return output


def resolve_file(path: str, formatter: Callable[[int, str], str] = tab_format) -> str:
    """Read a JSON file of dependencies and return a string formatted using the given formatter

    Arguments:
        path (str): The path of the file to read
        formatter (Callable[[int, str], str]): The formatter to use. It's a function that takes the indentation level
         and current dependency name, returning a formatted string

    Returns:
        str: formatted dependency graph
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} does not exist!")

    with open(path) as fd:
        parsed_json = parse_json(fd)
        return format_dependency_graph(parsed_json, formatter)

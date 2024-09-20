#!/usr/bin/env python3
from functools import partial
from typing import Callable


def space_format(spaces: int, indent: int, current: str) -> str:
    """Indents the given package name using spaces. Meant to be used through `make_space_formatter`.

    Arguments:
        spaces (int): number of spaces / indent level
        indent (int): the indentation level of the current package
        current (str): the name of the current package

    Returns:
        str: a string in the format of `' '*spaces*indent + " - {current}\n"`
    """
    return f"{' '*spaces*indent} - {current}\n"


def tab_format(indent: int, current: str) -> str:
    """Indents the given package name using tabs

    Arguments:
        indent (int): current indentation level
        current (str): the name of the current package

    Returns:
         str: a string in the format of `'\t'*indent + " - {current}\n"`
    """
    return f"{'\t'*indent} - {current}\n"


def make_space_formatter(space_per_indent: int) -> Callable[[int, str], str]:
    """Constructs a space_formatter with given configuration, making it possible to use with the dependency resolver.

    Arguments:
        space_per_indent (int): the number of spaces to place per indentation level

    Returns:
        Callable[[int, str], str]: a formatter function taking
          just the indentation level and current package name as parameters
    """
    return partial(space_format, space_per_indent)

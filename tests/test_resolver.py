import pytest

from tsa_two.dependency_resolver.exceptions import (
    DependencyCycleError,
    DependencyNotDefinedError,
)
from tsa_two.dependency_resolver.resolver import format_dependency_graph, resolve_file


def test_simple_valid_tree():
    """Check the correct formatting of a simple tree"""
    inpt = {"x": ["a"], "a": []}
    output = format_dependency_graph(inpt)
    assert output == " - x\n\t - a\n - a\n"


def test_missing_definition():
    """Check whether an exception is raised when an undefined package is referenced"""
    inpt = {"x": ["a", "b"], "a": []}

    with pytest.raises(DependencyNotDefinedError):
        format_dependency_graph(inpt)


def test_cycle():
    """Check whether an exception is raised when a dependency cycle is detected"""
    inpt = {"x": ["a", "b"], "b": ["x"], "a": []}
    with pytest.raises(DependencyCycleError):
        format_dependency_graph(inpt)


def test_selfloop():
    """Check whether an exception is raised when a self-loop is detected"""
    inpt = {"x": ["x"]}
    with pytest.raises(DependencyCycleError):
        format_dependency_graph(inpt)


def test_file_read():
    """Check whether a dependency tree read for a valid JSON file is formatted correctly"""
    result = resolve_file("tests/data/sample.json")
    assert result == " - a\n\t - b\n\t\t - c\n\t - c\n - b\n\t - c\n - c\n"


def test_file_read_dne():
    """Check that an exception is raised when the file cannot be found"""
    with pytest.raises(FileNotFoundError):
        resolve_file("THISFILLECANNOTEXISTASAASAAAAA")

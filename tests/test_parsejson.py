from io import StringIO

import pytest

from tsa_two.dependency_resolver.exceptions import DependencyJSONError
from tsa_two.dependency_resolver.resolver import parse_json


def test_valid_json():
    """Check the parsing of valid JSON"""
    inpt = StringIO('{"pkg1": ["a", "b", "c"]}')

    out = parse_json(inpt)

    assert "pkg1" in out
    assert out.get("pkg1") == ["a", "b", "c"]


def test_valid_json_str_int():
    """Check whether ints as dependencies are properly handled"""
    inpt = StringIO(
        '{"pkg1": [1, "b", "c", 3], "2": ["a", "b", "c"], "pkg3": [1, 3], "pkg4": ["a", "b"]}'
    )

    parse_json(inpt)


def test_incorrect_format_dict():
    """Check whether an exception is raised if the dependencies are an object/dict instead of a list"""
    with pytest.raises(DependencyJSONError):
        inpt = StringIO('{"x": {"a": [1, 2, 3]}}')
        parse_json(inpt)


def test_incorrect_format_array():
    """Check whether an exception is raised if the top-level type is list not dict"""
    with pytest.raises(DependencyJSONError):
        inpt = StringIO('[{"pkg1": ["a", "b", "c"]}]')
        parse_json(inpt)


def test_incorrect_format_deps():
    """Check whether an exception is raised if an object is included as a dependency for a package"""
    with pytest.raises(DependencyJSONError):
        inpt = StringIO('{"x": [{"a": 2}]}')
        parse_json(inpt)

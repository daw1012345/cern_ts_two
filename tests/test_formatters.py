from tsa_two.dependency_resolver.formatters import (
    make_space_formatter,
    space_format,
    tab_format,
)

# These tests are really simple - there are not really any edge-cases possible with the formatters
# These tests only validate the correct behavior of the formatters


def test_space_formatter():
    """Check normal functionality of the space formatter"""
    output = space_format(2, 10, "x")
    assert output == f"{' '*20} - x\n"


def test_space_formatter_factory():
    """Check normal functionality of the space formatter factory"""
    formatter = make_space_formatter(2)
    output = formatter(1, "x")
    assert output == "   - x\n"


def test_tab_factory():
    """Check normal functionality of the tab formatter"""
    output = tab_format(20, "x")
    assert output == f"{'\t'*20} - x\n"

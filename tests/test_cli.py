from io import StringIO

import pytest

from tsa_two.cli import main


def test_can_specify_spaces():
    """Check whether the spaces argument works"""
    buf = StringIO()

    main(args=["--spaces", "1", "tests/data/sample.json"], file=buf)
    output = buf.getvalue().splitlines()

    assert len(output) == 8
    assert output[0] == " - a"
    assert output[1] == "  - b"
    assert output[2] == "   - c"
    assert output[3] == "  - c"
    assert output[4] == " - b"
    assert output[5] == "  - c"
    assert output[6] == " - c"
    assert output[7] == ""


def test_normal_use():
    """Check normal usage of CLI utility"""
    buf = StringIO()

    main(args=["tests/data/sample.json"], file=buf)
    output = buf.getvalue().splitlines()

    assert len(output) == 8
    assert output[0] == " - a"
    assert output[1] == "\t - b"
    assert output[2] == "\t\t - c"
    assert output[3] == "\t - c"
    assert output[4] == " - b"
    assert output[5] == "\t - c"
    assert output[6] == " - c"
    assert output[7] == ""


def test_file_not_found_propagates():
    """Check behavior of CLI when incorrect path is given"""
    buf = StringIO()

    main(args=["THISFILEDOESNOTEXISTAAA"], file=buf)

    assert "Error:" in buf.getvalue()


def test_dependency_cycle_propagates():
    """Check proper handling of a cycle detected error"""
    buf = StringIO()

    main(args=["tests/data/sample_cycle.json"], file=buf)

    assert "cycle" in buf.getvalue()


def test_dependency_undefined_propagates():
    """Check the proper handling of packages referencing an undefined package"""
    buf = StringIO()

    main(args=["tests/data/sample_undef.json"], file=buf)

    assert "not defined" in buf.getvalue()


def test_invalid_format_propagates():
    """Check the proper handling of ill-formatted JSON"""
    buf = StringIO()

    main(args=["tests/data/sample_badtype.json"], file=buf)

    assert "wrong types" in buf.getvalue()


def test_invalid_json():
    """Check the proper handling of completely incorrect JSON.
    Specifically, JSON that cannot be parsed at all as JSON"""
    buf = StringIO()

    main(args=["tests/data/sample_badjson.json"], file=buf)

    assert "could not be parsed" in buf.getvalue()


def test_tabs_spaces_mutually_excl():
    """Check that the spaces and tabs formatters are mutually exclusive"""
    buf = StringIO()
    with pytest.raises(SystemExit):
        main(args=["--tabs", "--spaces", "2", "tests/data/sample.json"], file=buf)

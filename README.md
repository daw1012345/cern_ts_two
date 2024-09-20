# CERN Technical Student Assignment - Question 2
## Requirements
- Python >= 3.12
- No other dependencies
## Installation
- `pip3 install .`

## Running
- `tsa_two-cli <path>` OR `python3 -m tsa_two <path>`
- Optionally, specify a tab/space formatter for the output (tab formatter by default)

## Usage
```sh
usage: tsa_two-cli [-h] [--tabs | --spaces SPACES] path

positional arguments:
  path

options:
  -h, --help       show this help message and exit
  --tabs           Enable the tab formatter
  --spaces SPACES  Enable the space formatter with X spaces / indent
```

## Assumptions
- A dependency cycle is invalid
  - When a cycle is detected, the program stops traversing the dependency graph, reports an error and quits
- A package must exist to be declared as a dependency
  - If a package is declared as a dependency, but does not exist as a key in the JSON file, the program reports an error and exits
- A dependency in a dependency list must be a string or an integer
  - For example: `{"1": [2, "a"], "2": [], "a": []}` is valid - `2` can be (and is internally) converted into a string
  - Other types (such as an object, array or bool) cannot be converted into a string in an intuitive way
- The top-level type in the JSON file must be an object/dictionary

## Contributing and Code Quality
- If you wish to contribute, fork the project and create a PR
- A GitHub workflow will automatically lint and test your code. Requirements:
  - Passes Black lint
  - Passes isort lint
  - Passes flake8 lint
  - All tests pass, 80%+ test coverage
- **It is recommended that you install the provided pre-commit hooks**

## Manual linting/testing/formatting
First, install all the development dependencies with `pip install '.[dev]'`
- Black: `black .`
- isort: `isort .`
- flake8: `flake8`
- pytest: `pytest --doctest-modules --cov-fail-under=80 --junitxml=junit/test-results.xml --cov=src --cov-report=xml --cov-report=html`
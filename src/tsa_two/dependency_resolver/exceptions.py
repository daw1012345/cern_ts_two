#!/usr/bin/env python3
class DependencyCycleError(Exception):
    """Exception thrown when a cycle is found while traversing dependency graph"""

    pass


class DependencyNotDefinedError(Exception):
    """Exception is thrown when a package listed as a dependency is not defined"""

    pass


class DependencyJSONError(Exception):
    """Exception is thrown when the JSON format is valid, but its schema is not
    (e.g.: invalid types, format not followed)"""

    pass

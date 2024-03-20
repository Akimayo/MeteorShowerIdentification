"""
Defines functions which run the D-criteria calculations.
"""

from collections.abc import Callable
from typing import Any
from . import ast
from . import criteria
import threading
import sys
from lib.stdout import print_error_all

Runner = Callable[[],None]

def run_compare_single(orbit: ast.Orbit, ref, options: dict[str,Any]) -> tuple[Runner, list[ast.Result]]:
    result = ast.Result()
    return (lambda: _actual_run_compare_single(
        orbit,
        ref,
        options['criteria'] if 'criteria' in options else None,
        result
    ), [result])

def _actual_run_compare_single(orbit: ast.Orbit, reader, methods: list[str]|None, result: ast.Result):
    data = threading.local()
    while True:
        try:
            data.ref = next(reader)
            data.ref_instance = ast.Orbit.from_a(float(data.ref[1]), float(data.ref[2]), float(data.ref[3]), float(data.ref[5]), float(data.ref[4])).with_name(data.ref[0])
            for m in (criteria.ALL_CRITERIA if methods is None else filter(lambda m: m in criteria.ALL_CRITERIA, methods)):
                result[data.ref_instance.name or str(data.ref_instance)] = criteria.CRITERIA[m](orbit, data.ref_instance)
        except ValueError as fpe:
            print_error_all('Malformed input file', [''.join(data.ref), str(fpe)])
        except StopIteration:
            sys.exit()
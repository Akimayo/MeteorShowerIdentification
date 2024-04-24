"""
Defines functions which run the D-criteria calculations.
"""

from collections.abc import Callable,Iterable
from typing import Any
from . import ast
from . import criteria
import threading
import sys
from lib.stdout import print_warn_all
from lib import parser
from lib.io import FileStream

Runner = Callable[[],None]

def _try_get_criteria(options: dict[str,Any]) -> Iterable[str]:
    if 'criteria' in options:
        return filter(lambda m: m in criteria.ALL_CRITERIA, options['criteria'])
    else: return criteria.ALL_CRITERIA

def run_compare_single(orbit: ast.Orbit, parser: parser.Parser, options: dict[str,Any]) -> tuple[Runner, list[ast.Result]]:
    result = ast.Result(orbit)
    return (lambda: _actual_run_compare_single(
        orbit,
        parser,
        _try_get_criteria(options),
        result
    ), [result])

def _actual_run_compare_single(orbit: ast.Orbit, parser: parser.Parser, methods: Iterable[str], result: ast.Result):
    data = threading.local()
    data.orbit = None
    while True:
        try:
            data.orbit = next(parser)
            for m in methods:
                result[data.orbit.name or str(data.orbit)] = criteria.CRITERIA[m](orbit, data.orbit)
        except StopIteration:
            # Exit thread once no more reference orbits are available
            sys.exit()
        except ValueError as fpe:
            # Typically a FloatingPointError when float(...) gets invalid value
            print_warn_all('Malformed reference file line, skipping', [str(fpe), 'last successfully parsed was ' + str(data.orbit)])
            raise fpe
        except Exception as ex:
            print_warn_all('Something is wring with reference file, skipping line', [str(ex), 'last successfully parsed was ' + str(data.orbit)])
            raise ex

def run_compare_multiple(orbits: list[ast.Orbit], parser: parser.Parser, options: dict[str,Any]) -> tuple[Runner, list[ast.Result]]:
    results = list(map(lambda o: ast.Result(o), orbits))
    return (lambda: _actual_run_compare_multiple(
        orbits,
        parser,
        _try_get_criteria(options),
        results
    ), results)

def _actual_run_compare_multiple(orbits: list[ast.Orbit], parser: parser.Parser, methods: Iterable[str], results: list[ast.Result]):
    data = threading.local()
    data.orbit = None
    data.iter = range(len(orbits))
    while True:
        try:
            data.reference = next(parser)
            for i in data.iter:
                data.compared = orbits[i]
                for m in methods:
                    results[i][data.reference.name or str(data.reference)] = criteria.CRITERIA[m](data.compared, data.reference)
        except StopIteration:
            # Exit thread once no more reference orbits are available
            sys.exit()
        except ValueError as fpe:
            # Typically a FloatingPointError when float(...) gets invalid value
            print_warn_all('Malformed reference file line, skipping', [str(fpe), 'last successfully parsed was ' + str(orbits[-1])])
            raise fpe
        except Exception as ex:
            print_warn_all('Something is wrong with reference file, skipping line', [str(ex), 'last succesfully parsed was ' + str(data.orbit)])
            raise ex
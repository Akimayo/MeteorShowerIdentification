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
        except Exception as ex:
            print_warn_all('Something is wring with reference file, skipping line', [str(ex), 'last successfully parsed was ' + str(data.orbit)])

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
        except Exception as ex:
            print_warn_all('Something is wrong with reference file, skipping line', [str(ex), 'last succesfully parsed was ' + str(data.orbit)])
        
def run_compare_self(orbits: list[ast.Orbit], results: list[ast.Result], options: dict[str,Any]):
    return lambda: _actual_run_compare_self(
        orbits,
        _try_get_criteria(options),
        results
    )

def _actual_run_compare_self(orbits: list[ast.Orbit], methods: Iterable[str], results: list[ast.Result]):
    count = len(orbits)
    for i in range(count - 1):
        for j in range(i+1, count):
            for m in methods:
                results[i][orbits[j].name or str(orbits[j])] = criteria.CRITERIA[m](orbits[i], orbits[j])
    sys.exit()

def run_serial_assoc(file: FileStream, eof: int, positions: dict[str,int], options: dict[str,Any]):
    return lambda: _actual_run_serial_assoc(
        file,
        eof,
        positions,
        int(options['min_stream']) if 'min_stream' in 'options' else 1 
    )

def _actual_run_serial_assoc(file: FileStream, eof: int, positions: dict[str,int], min_stream: int):
    # Not using `threading.local()` here as this should only ever be run on one thread
    pos = positions.copy()
    queue = []
    try:
        while key := pos.keys().__iter__().__next__(): # Iterates results which have not yet been associated
            shower = ast.Shower(key)
            queue.append(key)
            try: # Hack for more efficient queue iteration (doesn't need to count items in list every iteration)
                while True: # Iterates through queue of orbits in this shower
                    key = queue.pop(0)
                    if not key in pos: continue # Prevent crashes when duplicate orbit names are present
                    file.seek(pos[key])
                    while line := file.readline(): # Iterates through lines of result
                        if line[:2] != '✔️': break # Get only accepted orbits; the checkmark is two characters
                        name = line[3:line.find('\t', 3)]
                        queue.append(name)
                        shower.orbits.append(name)
                    pos.__delitem__(key)
            except IndexError:
                pass
            if len(shower.orbits) > min_stream:
                file.seek(eof)
                file.write(str(shower))
                eof = file.tell()
    except StopIteration:
        sys.exit()
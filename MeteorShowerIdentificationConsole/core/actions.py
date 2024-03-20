"""
Provides functional actions for meteor shower identification tasks.
"""

from collections.abc import Callable
from lib import io
from . import ast
type Action = Callable[[io.InputSpecification, io.InputSpecification, dict], list[ast.Result]]
from lib.stdout import print_working, print_working_sub, progress
import threading
from . import runners
from time import sleep

_THREAD_COUNT = 4

def compare_single_with_file_action(orbit: io.InputSpecification, file: io.InputSpecification, options: dict) -> list[ast.Result]:
    if not isinstance(orbit, dict): raise TypeError('The value of `orbit` should be a dictionary')
    if not isinstance(file, str): raise TypeError('The value of `file` should be a string')
    orbit_instance = ast.Orbit.from_a(
        orbit['a'], orbit['e'], orbit['i'], orbit['w'], orbit['o']
    ) if options['dist'] == 'axis' else ast.Orbit.from_q(
        orbit['q'], orbit['e'], orbit['i'], orbit['w'], orbit['o']
    )

    print_working_sub('Working with orbit ' + str(orbit_instance))
    reader = io.get_reference_file(file)
    func, results = runners.run_compare_single(orbit_instance, reader, options)
    threads_on_start = threading.active_count()
    for n in range(_THREAD_COUNT):
        t = threading.Thread(target=func, name=(f'compare_single {n}'))
        t.start()
    
    p = progress('Comparing orbit with reference orbits')
    threads = threading.active_count()
    while threads > threads_on_start:
        sleep(0.2)
        threads = threading.active_count()
        p.animate(threads - 1)
    p.end()

    return results

def compare_file_with_file_action(file_compare: io.InputSpecification, file_with: io.InputSpecification, options: dict) -> list[ast.Result]:
    return []
    pass

def compare_file_with_self_action(file: io.InputSpecification, _, options: dict) -> list[ast.Result]:
    return []
    pass
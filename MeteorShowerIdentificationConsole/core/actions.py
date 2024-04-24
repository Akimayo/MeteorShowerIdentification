"""
Provides functional actions for meteor shower identification tasks.
"""

from lib import parser
from . import ast
from lib.stdout import print_working, print_warn_all, progress
import threading
from . import runners
from time import sleep
from lib.io import get_output_stream

_THREAD_COUNT = 8
_LOAD_AT_ONCE = 100

def compare_single_with_file_action(compared_orbit: parser.OrbitRef, reference_parser: parser.Parser, options: dict) -> None:
    """Compares a single orbit defined by its orbital elements in `compared_orbit` with reference orbits."""
    # Create `ast.Orbit` instance from CLI arguments
    orbit_instance = ast.Orbit.from_a(
        compared_orbit['a'], compared_orbit['e'], compared_orbit['i'], compared_orbit['w'], compared_orbit['o']
    ) if options['dist'] == 'axis' else ast.Orbit.from_q(
        compared_orbit['q'], compared_orbit['e'], compared_orbit['i'], compared_orbit['w'], compared_orbit['o']
    )

    print_working('Comparing orbit ' + str(orbit_instance))
    # Build multi-threaded comparer
    func, results = runners.run_compare_single(orbit_instance, reference_parser, options)
    threads_on_start = threading.active_count()
    for n in range(_THREAD_COUNT):
        t = threading.Thread(target=func, name=(f'compare_single {n}'))
        t.start()
    
    # Wait for comparisons to conclude and display processing animation
    p = progress('Comparing orbit with reference orbits')
    threads = threading.active_count()
    while threads > threads_on_start:
        sleep(0.2)
        threads = threading.active_count()
        p.animate(threads - 1)
    p.end('Compared orbit with reference orbits')

    output = get_output_stream()
    output.write(str(results[0]))

def compare_file_with_file_action(compared_parser: parser.Parser, reference_parser: parser.Parser, options: dict) -> None:
    """Compares each orbit in a file with reference orbits."""
    orbits = []
    total = 0
    count = 0
    output = get_output_stream()
    has_more = True
    print_working('Let\'s go!')
    while has_more: # Repeat until end of compared file is reached
        try:
            orbits = []
            count = 0

            # Load `_LOAD_AT_ONCE` lines from compared file
            for n in range(_LOAD_AT_ONCE):
                try:
                    orbits.append(next(compared_parser))
                    count += 1
                except StopIteration:
                    has_more = False
                    break
                except ValueError as fpe:
                    print_warn_all('Malformed compared file line, skipping', [str(fpe), 'last successfully parsed was ' + str(orbits[-1])])
                except Exception as ex:
                    print_warn_all('Something is wrong with compared file, skipping line', [str(ex), 'last successfully parsed was ' + str(orbits[-1])])
            total += count

            # Build multi-threaded comparer for this set of orbits
            func, res = runners.run_compare_multiple(orbits, reference_parser, options)
            threads_on_start = threading.active_count()
            for n in range(_THREAD_COUNT):
                t = threading.Thread(target=func, name=(f'compare_file {n}'))
                t.start()

            # Wait for comparisons to conclude and display processing animation
            p = progress(f'Comparing {count} orbits with reference orbits')
            threads = threading.active_count()
            while threads > threads_on_start:
                sleep(0.2)
                threads = threading.active_count()
                p.animate(threads - 1)
            
            for r in res:
                output.write(str(r))
            reference_parser.top()
            p.end(f'Compared {total} orbits with reference orbits')
        except StopIteration:
            break

def compare_file_with_self_action(parser: parser.Parser, parser_copy: parser.Parser, options: dict) -> None:
    """Compares orbits in a file with each other and performs serial association to identify meteor showers."""
    orbits = []
    total = 0
    count = 0
    file_positions: dict[str,int] = {}
    output = get_output_stream()
    has_more = True
    print_working('Let\'s go!')
    while has_more: # Repeat until end of file
        orbits = []
        count = 0
        # Load `_LOAD_AT_ONCE` lines from compared file

        for _ in range(_LOAD_AT_ONCE):
            try:
                orbits.append(next(parser))
                count += 1
            except StopIteration:
                has_more = False
                break
            except ValueError as fpe:
                print_warn_all('Malformed compared file line, skipping', [str(fpe), 'last successfully parsed was ' + str(orbits[-1])])
            except Exception as ex:
                print_warn_all('Something is wrong with compared file, skipping line', [str(ex), 'last successfully parsed was ' + str(orbits[-1])])
        total += count

        # Move the secondary stream to start of next block
        parser_copy.stream.seek(parser.stream.tell())

        # Build multi-threaded comparer for comparing this set of orbits with _the rest of the file_
        func, res = runners.run_compare_multiple(orbits, parser_copy, options)
        threads_on_start = threading.active_count()
        for n in range(_THREAD_COUNT - 1):
            threading.Thread(target=func, name=f'compare_self {n}').start()
        
        # Build multi-threaded comparer for comparing this set of orbits with _each other_
        func = runners.run_compare_self(orbits, res, options)
        threading.Thread(target=func, name='compare_self self').start()

        # Wait for comparisons on following vlocks to conclude and display processing animation
        p = progress(f'Comparing {count} orbits with each other')
        threads = threading.active_count()
        while threads > threads_on_start:
            sleep(0.2)
            threads = threading.active_count()
            p.animate(_THREAD_COUNT - 1)

        for r in res:
            file_positions[r.orbit.name or str(r.orbit)] = output.tell() + r.HEADER_LENGTH + 1 # Save positions of results in file for serial association
            output.write(str(r))
        p.end(f'Compared {total} orbits with each other')

    # Prepare for serial association search
    p = progress('Performing serial association of meteor showers')
    out_eof = output.tell()
    output.seek(0)
    func = runners.run_serial_assoc(output, out_eof, file_positions, options)

    # Start serial association thread, wait for it to end, and display processing animation
    t = threading.Thread(target=func, name='compare_self assoc')
    t.start()
    while t.is_alive():
        sleep(0.2)
        p.animate()
    p.end('Finished serial association search of meteor showers')
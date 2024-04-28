from colorama import just_fix_windows_console, Fore, Style
from meta.cliargs import get_runner, print_help
from lib.stdout import print_info_sub, print_error, print_error_all, print_success, print_success_sub, print_error_sub, _use_verbose
from meta.config import create_config
from core.actions import compare_file_with_file_action, compare_file_with_self_action, compare_single_with_file_action
from lib.io import preload, get_output_stream, release_output_stream
from lib.parser import Parser
from time import time
from sys import exit

just_fix_windows_console() # Let `colorama` apply fixes for Windows console to display colors etc.

try:
    # Get options from command-line arguments and .meteorrc
    options = get_runner()
    print_info_sub('Proceeding with launch options ' + Style.DIM + options.__str__() + Style.RESET_ALL, True)

    if not 'action' in options:
        print_error('No action specified. Use ' + Style.DIM + Fore.YELLOW + '--help' + Fore.RESET + Style.RESET_ALL + ' to list uses.')
        exit(1)

    # Run action determined from args or .meteorrc
    match options['action']:
        case 'write_help': print_help()
        case 'generate_config': create_config('force' in options and bool(options['force']))
        case _: # Catch for the actual actions with common code
            # Check and open input and output files
            p_compared, p_reference = preload(options)
            output = get_output_stream(options)

            # Select and run action
            start = time()
            match options['action']:
                case 'compare_single': # Compare a single orbit given via arguments with a reference orbits file
                    if not type(p_compared) is dict: raise TypeError('Should have gotten a dictionary as compared orbit specification', type(p_compared))
                    if not isinstance(p_reference, Parser): raise Exception('Should have gotten a parser as reference orbit source', type(p_reference))
                    results = compare_single_with_file_action(p_compared, p_reference, options)
                    p_reference.stream.close()
                case 'compare_file': # Compare a file of orbits with a reference orbits file
                    if not isinstance(p_compared, Parser): raise TypeError('Should have gotten a parser as compared orbit source', type(p_compared))
                    if not isinstance(p_reference, Parser): raise TypeError('Should have gotten a parser as reference orbit source', type(p_reference))
                    results = compare_file_with_file_action(p_compared, p_reference, options)
                    p_compared.stream.close()
                    p_reference.stream.close()
                case 'compare_self': # Compare a file of orbits with itself and use serial association to find showers
                    if not (isinstance(p_compared, Parser) and isinstance(p_reference, Parser)): raise Exception('Should have gotten a parser as orbit source', type(p_compared))
                    results = compare_file_with_self_action(p_compared, p_reference, options)
                    p_compared.stream.close()
                    p_reference.stream.close()
                case _: raise ValueError(str(options['action']) + ' is not supported')
            end = time()

            print_success('Orbit comparison completed')
            print_success_sub('Took ' + str(round(end - start, 2)) + 's', True)
            release_output_stream()
            print_success('Results written to ' + ('console' if not 'output' in options or options['output'] is None else (Style.DIM + str(options['output']) + Style.RESET_ALL)))
except Exception as ex:
    # When any unhandled exception occurs, print it out formatted
    print_error_all(ex.__doc__ or ex.__str__(), list(ex.args))
    # Write a hint about `--verbose` when not used
    if not _use_verbose: print_error_sub('If you\'re stuck, try running the command with the ' + Fore.YELLOW + '--verbose' + Fore.RESET + ' flag to get more information.')
    exit(-1)
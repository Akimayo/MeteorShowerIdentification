from colorama import just_fix_windows_console, Fore, Style
from meta.cliargs import get_runner, print_help
from lib.stdout import print_info_sub, print_error, print_error_all, _use_verbose
from meta.config import create_config
from core.actions import Action, compare_file_with_file_action, compare_file_with_self_action, compare_single_with_file_action
from lib.io import preload

just_fix_windows_console()

actions: dict[str, Action] = {
    'compare_single': compare_single_with_file_action,
    'compare_file': compare_file_with_file_action,
    'compare_self': compare_file_with_self_action
}

try:
    options = get_runner()
    print_info_sub('Proceeding with launch options ' + Style.DIM + options.__str__() + Style.RESET_ALL, True)

    if not 'action' in options:
        print_error('No action specified. Use ' + Style.DIM + Fore.YELLOW + '--help' + Fore.RESET + Style.RESET_ALL + ' to list uses.')
        exit(1)

    match options['action']:
        case 'write_help': print_help()
        case 'generate_config': create_config('force' in options and bool(options['force']))
        case _:
            d_compare, d_with = preload(options)
            exec = actions[str(options['action'])]
            results = exec(d_compare, d_with, options)
            print('\n'.join(map(lambda r: str(r), results)))
except Exception as ex:
    print_error_all(ex.__doc__ or ex.__str__(), list(ex.args))
    exit(-1)
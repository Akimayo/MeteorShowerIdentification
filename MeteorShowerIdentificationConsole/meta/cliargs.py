"""
Provides the `get_runner()` method, which parses command-line arguments passed to the
script and returns an object containing the given launch settings (including settings
declared in the configuration file), and the `print_help()` method.
"""
import sys
from lib import stdout
from . import config
from colorama import Style

#region Option methods
def _opt_config(launch_options): 
    """Sets the action to `generate_config`."""
    launch_options['action'] = 'generate_config'

def _opt_ignore_config(launch_options):
    """Tells the script to disregard settings in the `.meteorrc` config file."""
    launch_options['use_config'] = False

def _opt_help(launch_options):
    """Sets the action to `write_help`."""
    launch_options['action'] = 'write_help'

def _opt_eccentricity(launch_options, e):
    """Set eccentricity of compared orbit and set action to `compare_single`."""
    launch_options['data']['compare']['e'] = float(e)
    launch_options['action'] = 'compare_single'

def _opt_perihelion_distance(launch_options, q):
    """Set perihelion of compared orbit, set distance mode to `apsis` and set action to `compare_single`."""
    launch_options['data']['compare']['q'] = float(q)
    # launch_options['dist'] = 'apsis'
    launch_options['action'] = 'compare_single'

def _opt_semimajor_axis(launch_options, a):
    """Set semimajor axis of compared orbit, set distance mode to `axis` and set action to `compare_single`."""
    launch_options['data']['compare']['a'] = float(a)
    # launch_options['dist'] = 'axis'
    launch_options['action'] = 'compare_single'

def _opt_inclination(launch_options, i):
    """Set inclination of compared orbit and set action to `compare_single`."""
    launch_options['data']['compare']['i'] = float(i)
    launch_options['action'] = 'compare_single'

def _opt_perihelion_arg(launch_options, w):
    """Set argument of perihelion of compared orbit and set action to `compare_single`."""
    launch_options['data']['compare']['w'] = float(w)
    launch_options['action'] = 'compare_single'

def _opt_asc_node_lat(launch_options, o):
    """Set latitude of ascending node of compared orbit and set action to `compare_single`."""
    launch_options['data']['compare']['o'] = float(o)
    launch_options['action'] = 'compare_single'

def _opt_criteria(launch_options, criteria):
    """Set D-criteria to be used."""
    launch_options['criteria'] = criteria.split(',')

def _opt_output(launch_options, path):
    """Set output file path."""
    launch_options['output'] = path

# def _opt_distance(launch_options, dist):
#     """Set distance mode."""
#     if 'dist' in launch_options:
#         raise AssertionError('Distance type has already been set by another option.')
#     if dist == 'apsis' or dist == 'axis':
#         launch_options['dist'] = dist
#     else:
#         raise ValueError('Use the --distance parameter with either "axis" or "apsis".')

def _opt_verbose(_):
    """Enable verbose output."""
    stdout.use_verbose()

def _opt_force(launch_options):
    """Forces a potentially unsafe action."""
    launch_options['force'] = True
#endregion

OPTIONS = {
    # Generate a config file
    '--config': { 'val': None, 'invoke': _opt_config }, '-c': { 'val': None, 'invoke': _opt_config },
    # Ignore config, use only args
    '-0': { 'val': None, 'invoke': _opt_ignore_config },
    # Write help
    '--help': { 'val': None, 'invoke': _opt_help }, '-h': { 'val': None, 'invoke': _opt_help },
    # Set orbit eccentricity
    '-e': { 'val': 'eccentricity', 'invoke': _opt_eccentricity },
    # Set perihelion distance
    '-q': { 'val': 'perihel_dist', 'invoke': _opt_perihelion_distance },
    # Set semimajor axis
    '-a': { 'val': 'smajor_axis', 'invoke': _opt_semimajor_axis },
    # Set inclination
    '-i': { 'val': 'inclination', 'invoke': _opt_inclination },
    # Set argument of perihelion
    '-w': { 'val': 'arg_perihel', 'invoke': _opt_perihelion_arg },
    # Set latitude of ascending node
    '-O': { 'val': 'asc_lat', 'invoke': _opt_asc_node_lat },
    # Set list of used D-criteria
    '--criteria': { 'val': 'criteria', 'invoke': _opt_criteria }, '-r': { 'val': 'criteria', 'invoke': _opt_criteria },
    # Set output location
    '--output': { 'val': 'path', 'invoke': _opt_output }, '-o': { 'val': 'path', 'invoke': _opt_output },
    # Set distance measure type
    # '--distance': { 'val': '"apsis"|"axis"', 'invoke': _opt_distance }, '-d': { 'val': '"apsis"|"axis"', 'invoke': _opt_distance },
    # Enable verbose output
    '--verbose': { 'val': None, 'invoke': _opt_verbose },
    # Force a potentially unsafe operation
    '--force': { 'val': None, 'invoke': _opt_force }, '-f': { 'val': None, 'invoke': _opt_force } 
}

def get_runner():
    """Parses command-line arguments given to the script and a configuration file and returns a launch options object."""
    arg_options = { 'use_config': True, 'criteria': None, 'data': { 'compare': {} } }
    files = []
    next_update_option = None
    # Iterate `argv` to retrieve options
    for arg in sys.argv[1:]:
        if next_update_option:
            next_update_option(arg_options, arg)
            next_update_option = None
        elif arg in OPTIONS:
            opt = OPTIONS[arg]
            if opt['val']: next_update_option = opt['invoke']
            else: opt['invoke'](arg_options)
        else: files.append(arg)
    # Use lone strings as file inputs
    if len(files) > 1:
        arg_options['data']['compare'] = files[0]
        arg_options['data']['with'] = files[1]
        arg_options['action'] = 'compare_file'
    elif len(files) > 0:
        if not 'action' in arg_options:
            arg_options['data']['compare'] = files[0]
            arg_options['action'] = 'compare_self'
        else: arg_options['data']['with'] = files[0]
    
    # Load configuration or default options
    if arg_options['use_config'] and ('action' in arg_options and arg_options['action'] != 'write_help' or not 'action' in arg_options): launch_options = config.load_config()
    else: launch_options = config.DEFAULT_OPTIONS

    # Override configuration with values passed directly to script
    if 'action' in arg_options: launch_options['action'] = arg_options['action']
    if 'criteria' in arg_options and arg_options['criteria']: launch_options['criteria'] = arg_options['criteria']
    if 'data' in arg_options and len(arg_options['data']['compare']) > 0: launch_options['data'] = arg_options['data']
    if 'output' in arg_options: launch_options['output'] = arg_options['output']
    # if 'dist' in arg_options: launch_options['dist'] = arg_options['dist']
    if 'force' in arg_options: launch_options['force'] = arg_options['force']

    return launch_options

_optgroups = [
    {
        'title': 'Configuration',
        'options': [
            {
                'keys': ['--config', '-c'],
                'combined': True,
                'helpText': [
                    '  Creates a ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' configuration file',
                    'for the current directory.',
                    '  This file is in the YAML format.'
                ]
            },
            {
                'keys': ['-0'],
                'combined': True,
                'helpText': [
                    '  Disregard ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' configuration files.'
                ]
            }
        ]
    },
    {
        'title': 'Single Orbit',
        'options': [
            {
                'keys': ['-e', '-q', '-i', '-w', '-O'],
                'combined': False,
                'helpText': [
                    '  Set the orbital elements of a meteor orbit',
                    'with perihelion distance ' + Style.BRIGHT + 'q' + Style.RESET_ALL + '.'
                ]
            },
            {
                'keys': ['-e', '-a', '-i', '-w', '-O'],
                'combined': False,
                'helpText': [
                    '  Set the orbital elements of a meteor orbit',
                    'with semimajor axis length ' + Style.BRIGHT + 'a' + Style.RESET_ALL + '.'
                ]
            }
        ]
    },
    {
        'title': 'Input/Output',
        'options': [
            {
                'keys': ['--criteria', '-r'],
                'combined': True,
                'helpText': [
                    '  Set the D-criteria to be used.',
                    '  Takes a comma-separated list. Supported are',
                    'the follwing values: ' + ', '.join(map(lambda m: Style.DIM + '"' + m + '"' + Style.RESET_ALL, ['sh', 'd', 'h', 'n']))
                ]
            },
            # {
            #     'keys': ['--distance', '-d'],
            #     'combined': True,
            #     'helpText': [
            #         '  Set the distance type used in input files.',
            #         '  Use ' + Style.DIM + '"axis"' + Style.RESET_ALL + ' for semi-major axis length ' + Style.BRIGHT + 'a' + Style.RESET_ALL + ' or',
            #         Style.DIM + '"apsis"' + Style.RESET_ALL + ' for perihelion distance ' + Style.BRIGHT + 'q' + Style.RESET_ALL + '.',
            #         'Defaults to "' + config.DEFAULT_OPTIONS['dist'] + '".'
            #     ]
            # },
            {
                'keys': ['--output', '-o'],
                'combined': True,
                'helpText': [
                    '  Directs the results to a file. Omitting',
                    'this option will write results to the console.'
                ]
            }
        ]
    },
    {
        'title': 'Miscellaneous',
        'options': [
            {
                'keys': ['--force', '-f'],
                'combined': True,
                'helpText': [
                    'Forces a potentially unsafe operation.'
                ]
            },
            {
                'keys': ['--verbose'],
                'combined': True,
                'helpText': [
                    '  Enables verbose logging to console.'
                ]
            },
            {
                'keys': ['--help', '-h'],
                'combined': True,
                'helpText': [
                    'Prints this help text.'
                ]
            }
        ]
    }
]
def print_help():
    """Prints help text to console"""
    print(Style.BRIGHT + 'METEOR SHOWER IDENTIFICATION CONSOLE' + Style.RESET_ALL)
    print('meteors [<compared_file> [<reference_file>|"default"]] [...options]')
    for group in _optgroups:
        print('\n ' + Style.BRIGHT + group['title'] + Style.RESET_ALL)
        print('=' * (len(group['title']) + 2))
        for opt in group['options']:
            print(
                (', ' if opt['combined'] else '\n').join(
                    map(lambda key: key + ('' if not OPTIONS[key]['val'] else (Style.DIM + ' <' + OPTIONS[key]['val'] + '>' + Style.RESET_ALL)),
                        opt['keys'])
                )
            )
            for line in opt['helpText']:
                print('\t' + line)
    print(Style.RESET_ALL)
"""
Handles loading and writing of the `.meteorrc` configuration file.
"""
import yaml
from os import path
from lib import stdout
from lib.parser import ParserOptions
from colorama import Style, Fore
from typing import Any
from jsonschema import validate, ValidationError
from core import actions

DEFAULT_OPTIONS: dict[str,Any] = {
    'output': None
}

def get_parser_config(columns: dict[str,str]) -> ParserOptions:
    """Transform a dictionary from the configuration file into a `ParserOptions` instance."""
    parser = (ParserOptions().set_eccentricity(columns['eccentricity'])
                             .set_perihelion_argument(columns['perihelionArgument'])
                             .set_asc_node_longitude(columns['ascNodeLongitude'])
                             .set_inclination(columns['inclination']))
    if 'axisLength' in columns: parser.set_semimajor_axis_length(columns['axisLength'])
    if 'perihelionDistance' in columns: parser.set_perihelion_distance(columns['perihelionDistance'])
    if 'code' in columns: parser.set_code(columns['code'])
    if 'name' in columns: parser.set_name(columns['name'])
    return parser

def load_config() -> dict[str, str|dict|None]:
    """Try loading a config file. If the file does not exist, returns default options."""
    try:
        # Load the schema from internal files for validation
        schema_path = path.join(path.dirname(path.realpath(__file__)), '../constants/meteorrc-schema.json')
        with open(schema_path, 'r') as schema_stream:
            schema = yaml.safe_load(schema_stream)
        # Load the `.meteorrc` file
        with open('.meteorrc', 'r') as file:
            cfg = yaml.safe_load(file)
            filepath = path.abspath('./.meteorrc')

        # Validate the configuration file
        options = DEFAULT_OPTIONS.copy()
        if cfg is None: return options # When the config file is empty, skip validation
        validate(cfg, schema)

        # Copy configuration into internal options dictionary
        if 'criteria' in cfg:
            if isinstance(cfg['criteria'], dict):
                # Used criteria
                if 'use' in cfg['criteria']: options['criteria'] = cfg['criteria']['use']
                # Criteria cutoff limits
                if 'limits' in cfg['criteria']:
                    options['limits'] = {}
                    if 'sh' in cfg['criteria']['limits']: options['limits']['sh'] = tuple(cfg['criteria']['limits']['sh'].values())
                    if 'd' in cfg['criteria']['limits']: options['limits']['d'] = tuple(cfg['criteria']['limits']['d'].values())
                    if 'h' in cfg['criteria']['limits']: options['limits']['h'] = tuple(cfg['criteria']['limits']['h'].values())
                    if 'n' in cfg['criteria']['limits']: options['limits']['n'] = tuple(cfg['criteria']['limits']['n'].values())
            else:
                # Used criteria
                options['criteria'] = cfg['criteria']
        if 'inputs' in cfg:
            # Compared input file
            if 'compared' in cfg['inputs']:
                compared = cfg['inputs']['compared']
                # Path only
                if isinstance(compared, str):
                    options['compare_data'] = compared
                # Path and optionally columns specified
                elif 'path' in compared:
                    options['compare_data'] = compared['path']
                    if 'columns' in compared: options['parse_data'] = get_parser_config(compared['columns'])
                # Elements of a single orbit specified
                else:
                    options['compare_data'] = {
                        'e': compared['a'],
                        'i': compared['i'],
                        'o': compared['O'],
                        'w': compared['w']
                    }
                    if 'a' in compared:
                        options['compare_data']['a'] = compared['a']
                    else:
                        options['compare_data']['q'] = compared['q']
            # Reference input file
            if 'reference' in cfg['inputs']:
                reference = cfg['inputs']['reference']
                # Path only
                if isinstance(reference, str):
                    options['compare_with'] = reference
                # Path and optionally columns specified
                else:
                    options['compare_with'] = reference['path']
                    if 'columns' in reference:options['parse_with'] = get_parser_config(reference['columns'])
        if 'output' in cfg:
            options['output'] = cfg['output']
        if '_core' in cfg:
            # Optionally set the number of orbits loaded at once and number of threads to run on
            if 'load' in cfg['_core']: actions._LOAD_AT_ONCE = cfg['_core']['load']
            if 'threads' in cfg['_core']: actions._THREAD_COUNT = cfg['_core']['threads']

        stdout.print_config(filepath, cfg)

        return options
    except FileNotFoundError:
        # When `.meteorrc` does not exist, use defaults
        return DEFAULT_OPTIONS.copy()
    except ValidationError as ve:
        # When `.meteorrc` is not valid according to schema, tell the location of the invalid option
        stdout.print_error_all('The configuration file is not valid.', [
            ve.message,
            'at ' + ve.json_path
        ])
        raise AssertionError((ve.__doc__ or '').strip())
    
def create_config(force: bool = False):
    """Creates a config file containing default options."""
    stdout.print_info('Writing configuration file ' + Style.DIM + path.abspath('./.meteorrc') + Style.RESET_ALL)
    stdout.print_info_sub('Checking for an existing ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file...', True)
    # Check whether the configuration file exists first. If it does, and the `--force` flag is not used, don't proceed (return).
    if path.exists('./.meteorrc'):
        if force:
            stdout.print_warn_sub('Overwriting existing ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file because the ' +
                                  Fore.YELLOW + Style.DIM + '--force' + Style.RESET_ALL + Fore.RESET + ' flag was used')
        else:
            stdout.print_warn_all('A ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file is already present in this location', [
                'Use the ' + Fore.YELLOW + Style.DIM + '--force' + Style.RESET_ALL + Fore.RESET + ' flag to overwrite it.'
            ])
            return
    # Create a new `.meteorrc` file
    with open('.meteorrc', 'w') as file:
        stdout.print_info_sub('Creating the YAML configuration file...', True)
        # Write the `$schema` directive for smart editors (and three dashes, the start of a YAML document).
        file.writelines([
            "# yaml-language-server: $schema=https://raw.githubusercontent.com/Akimayo/MeteorShowerIdentification/master/MeteorShowerIdentificationConsole/constants/meteorrc-schema.json\n",
            "---\n", "\n"
        ])
        stdout.print_info_sub('Writing help comments...', True)
        # Write some comments for getting started
        file.writelines(map(lambda l: '# ' + l + '\n', [
            'GETTING STARTED:',
            'In a smart text editor, use the hints given by pressing [Ctrl]+[Space] to start writing the configuration file.',
            'Otherwise, navigate to the schema using the URL above and use it to learn how to structure the configuration file.',
            'All these options can be overriden by command-line arguments.',
            'You can try starting with the following options:',
            '`output` -- Write outputs to a certain file',
            '`inputs` -- Always use a certain (combination of) input file(s).',
            '`criteria` -- Select which D-criteria to use',
            'If you want to disable all the options in this configuration file, make sure to delete or comment out the `---`',
            'at the start of the document, otherwise it won\'t pass validation.'
        ]))
    stdout.print_success_all('Succesfully created a ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' configuration file', [
        'This configuration file will be used whenever this location is the current working directory.',
        'Open the ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file in your favourite smart editor and edit it as a YAML file.'
    ])
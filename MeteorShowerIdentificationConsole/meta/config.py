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
    'output': None,
    # 'dist': 'apsis'
}

def get_parser_config(columns: dict[str,str]) -> ParserOptions:
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
        schema_path = path.join(path.dirname(path.realpath(__file__)), '../constants/meteorrc-schema.json')
        with open(schema_path) as schema_stream:
            schema = yaml.safe_load(schema_stream)
        with open('.meteorrc', 'r') as file:
            cfg = yaml.safe_load(file)
            filepath = path.abspath('./.meteorrc')

        options = DEFAULT_OPTIONS.copy()
        if cfg is None: return options # When the config file is empty, skip validation
        validate(cfg, schema)

        if 'criteria' in cfg:
            if isinstance(cfg['criteria'], dict):
                if 'use' in cfg['criteria']: options['criteria'] = cfg['criteria']['use']
                if 'limits' in cfg['criteria']:
                    options['limits'] = {}
                    if 'sh' in cfg['criteria']['limits']: options['limits']['sh'] = tuple(cfg['criteria']['limits']['sh'].values())
                    if 'd' in cfg['criteria']['limits']: options['limits']['d'] = tuple(cfg['criteria']['limits']['d'].values())
                    if 'h' in cfg['criteria']['limits']: options['limits']['h'] = tuple(cfg['criteria']['limits']['h'].values())
                    if 'n' in cfg['criteria']['limits']: options['limits']['n'] = tuple(cfg['criteria']['limits']['n'].values())
            else:
                options['criteria'] = cfg['criteria']
        if 'inputs' in cfg:
            if 'compared' in cfg['inputs']:
                compared = cfg['inputs']['compared']
                if compared is str:
                    options['compare_data'] = compared
                elif 'path' in compared:
                    options['compare_data'] = compared['path']
                    options['parse_data'] = get_parser_config(compared['columns'])
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
            if 'reference' in cfg['inputs']:
                reference = cfg['inputs']['reference']
                if not reference is str:
                    options['compare_with'] = reference
                else:
                    options['compare_with'] = reference['path']
                    options['parse_with'] = get_parser_config(reference['columns'])
        if 'output' in cfg:
            options['output'] = cfg['output']
        if '_core' in cfg:
            if 'load' in cfg['_core']: actions._LOAD_AT_ONCE = cfg['_core']['load']
            if 'threads' in cfg['_core']: actions._THREAD_COUNT = cfg['_core']['threads']
        # if 'dist' in cfg: options['dist'] = cfg['dist']

        stdout.print_config(filepath, cfg)

        return options
    except FileNotFoundError:
        return DEFAULT_OPTIONS.copy()
    except ValidationError as ve:
        stdout.print_error_all('The configuration file is not valid.', [
            ve.message,
            'at ' + ve.json_path
        ])
        raise AssertionError((ve.__doc__ or '').strip())
    
def create_config(force: bool = False):
    """Creates a config file containing default options."""
    stdout.print_info('Writing configuration file ' + Style.DIM + path.abspath('./.meteorrc') + Style.RESET_ALL)
    stdout.print_info_sub('Checking for an existing ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file...', True)
    if path.exists('./.meteorrc'):
        if force:
            stdout.print_warn_sub('Overwriting existing ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file because the ' +
                                  Fore.YELLOW + Style.DIM + '--force' + Style.RESET_ALL + Fore.RESET + ' flag was used')
        else:
            stdout.print_warn_all('A ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file is already present in this location', [
                'Use the ' + Fore.YELLOW + Style.DIM + '--force' + Style.RESET_ALL + Fore.RESET + ' flag to overwrite it.'
            ])
            return
    with open('.meteorrc', 'w') as file:
        stdout.print_info_sub('Creating the YAML configuration file...', True)
        file.writelines([
            "# yaml-language-server: $schema=./MeteorShowerIdentificationConsole/constants/meteorrc-schema.json\n",
            "---\n", "\n"
        ])
        stdout.print_info_sub('Writing help comments...', True)
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
            # '`dist` -- distance type of input files, either "apis" for perihelion distance or "axis" for semimajor axis length'
        ]))
    stdout.print_success_all('Succesfully created a ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' configuration file', [
        'This configuration file will be used whenever this location is the current working directory.',
        'Open the ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file in your favourite smart editor and edit it as a YAML file.'
    ])
"""
Handles loading and writing of the `.meteorrc` configuration file.
"""
import yaml
from os import path
from lib import stdout
from colorama import Style, Fore

DEFAULT_OPTIONS = {
    'output': None,
    'dist': 'apsis'
}

def load_config() -> dict[str, str|dict|None]:
    """Try loading a config file. If the file does not exist, returns default options."""
    try:
        with open('.meteorrc', 'r') as file:
            cfg = yaml.safe_load(file)
            filepath = path.abspath('./.meteorrc')
        options = DEFAULT_OPTIONS.copy()

        if 'criteria' in cfg: options['criteria'] = cfg['criteria']
        if 'compare_data' in cfg: options['data']['compare'] = cfg['compare_data']
        if 'compare_with' in cfg: options['data']['with'] = cfg['compare_with']
        if 'output' in cfg: options['output'] = cfg['output']
        if 'dist' in cfg: options['dist'] = cfg['dist']

        stdout.print_config(filepath, cfg)

        return options
    except FileNotFoundError:
        return DEFAULT_OPTIONS.copy()
    
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
        stdout.print_info_sub('Writing default configuration in YAML format...', True)
        yaml.safe_dump(DEFAULT_OPTIONS, file)

        stdout.print_info_sub('Writing help comments...', True)
        file.writelines(map(lambda l: '# ' + l + '\n', [
            'SUPPORTED OPTIONS:',
            '`criteria` -- array of following options: "sh", "d", "h", "n"',
            '`compare_data` -- either a string path or an object specifying orbital elements',
            '`compare_with` -- either a string path or "default" for internal known orbit database',
            '`output` -- string path of output file or omit for stdout',
            '`dist` -- distance type of input files, either "apis" for perihelion distance or "axis" for semimajor axis length'
        ]))
    stdout.print_success_all('Succesfully created a ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' configuration file', [
        'This configuration file will be used whenever this location is the current working directory.',
        'Open the ' + Style.DIM + '.meteorrc' + Style.RESET_ALL + ' file in your favourite smart editor and edit it as a YAML file.'
    ])
"""
Provides tools for reading and writing files.
"""
from os import path
from . import stdout
from colorama import Style
from io import TextIOWrapper
from lib import parser
from tempfile import TemporaryFile, _TemporaryFileWrapper

type InputSpecification = parser.OrbitRef|parser.Parser|None
type FileStream = TextIOWrapper | _TemporaryFileWrapper[str]

_INTERNAL_DATA_FILE = 'SHOWERS.DAT'

def preload(options: dict) -> tuple[InputSpecification, InputSpecification]:
    """Checks input arguments, whether the files exist, and returns absolute paths or data"""
    parser1 = None; parser2 = None
    has_error = False
    stdout.print_info('Checking inputs...')

    # Compared file
    if type(options['data']['compare']) is dict:
        # When it is specified by parameters, use it as is
        parser1 = options['data']['compare']
        stdout.print_info_sub('Compared data specified explicitly', True)
    else:
        # When it is a string, check that the file exists
        cfile = path.abspath(options['data']['compare'])
        if path.exists(cfile):
            stdout.print_info_sub('Compared data in file ' + Style.DIM + cfile + Style.RESET_ALL, True)
            parser1 = parser.DatParser(open_stream(cfile), parser.FALLBACK_PARSER_OPTIONS) # FIXME: Use options to modify parser
            stdout.print_info_sub('Compared file has fields ' + str(parser1.get_fieldnames()), True)
        else:
            stdout.print_error('Compared data file ' + Style.DIM + cfile + Style.RESET_ALL + ' does not exist')
            has_error = True
    
    # Reference file
    if options['action'] == 'compare_self':
        # When it is not specified, e. g. the action is parsed as 'compare_self', do nothing
        if not has_error: stdout.print_info_sub('Comparing orbits with each other', True)
        parser2 = parser.DatParser(open_stream(cfile), parser.FALLBACK_PARSER_OPTIONS) # FIXME: Use options to modify parser # type:ignore
    elif 'with' in options['data']:
        # When a reference file ('with' parameter) is specified for any other action
        if options['data']['with'] == 'default':
            # When it is set to default, use the built-in database
            if not has_error: stdout.print_info_sub('Comparing with built-in meteor shower orbit database')
            wfile = path.join(path.dirname(path.realpath(__file__)), '../constants/', _INTERNAL_DATA_FILE)
            parser2 = parser.CsvParser(open_stream(wfile), parser.DEFAULT_DATASET_PARSER_OPTIONS)
        else:
            # When it is any other string, check that it exists
            wfile = path.abspath(options['data']['with'])
            if path.exists(wfile):
                if not has_error: stdout.print_info_sub('Reference data in file ' + Style.DIM + wfile + Style.RESET_ALL, True)
                parser2 = parser.DatParser(open_stream(wfile), parser.FALLBACK_PARSER_OPTIONS) # FIXME: Use options to modify parser
                stdout.print_info_sub('Reference file has fields ' + str(parser2.get_fieldnames()), True)
            else:
                stdout.print_error('Reference data file ' + Style.DIM + wfile + Style.RESET_ALL + ' does not exist')
                has_error = True
    else:
        # When it is not specified for any other action (which should not occur), fail
        stdout.print_error('Reference data file not specified')
        has_error = True

    if has_error: raise ValueError('Input files not properly specified')
    return parser1, parser2


def open_stream(path: str) -> TextIOWrapper:
    """Helper method for opening files."""
    return open(path, encoding='utf-8')

_outstream = None
def get_output_stream(options: dict|None = None) -> FileStream:
    """Returns a singleton stream of the output file (or a tempfile, which will be printed upon close)."""
    global _outstream
    if _outstream is None:
        if isinstance(options, dict):
            if isinstance(options['output'], str):
                _outstream = open(options['output'], 'w+' if 'force' in options and options['force'] else 'x+', encoding='utf-8')
            else:
                _outstream = TemporaryFile('w+t', encoding='utf-8')
        else: raise ValueError('Output file is not yet open and the options argument is None')
    return _outstream

def release_output_stream():
    global _outstream
    if not _outstream is None:
        if isinstance(_outstream, _TemporaryFileWrapper):
            _outstream.seek(0)
            for l in _outstream:
                print(l[:-1])
        _outstream.close()
        _outstream = None

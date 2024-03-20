"""
Provides tools for reading and writing files.
"""
from os import path
from . import stdout
from colorama import Style
import csv
import threading

type InputSpecification = dict[str,float]|str|None

def preload(options: dict) -> list[InputSpecification]:
    """Checks input arguments, whether the files exist, and returns absolute paths or data"""
    ret = []
    has_error = False
    stdout.print_info('Checking inputs...')

    # `compare` file
    if type(options['data']['compare']) is dict:
        # When it is specified by parameters, use it as is
        ret.append(options['data']['compare'])
        stdout.print_info_sub('Compared data specified explicitly', True)
    else:
        # When it is a string, check that the file exists
        cfile = path.abspath(options['data']['compare'])
        if path.exists(cfile):
            stdout.print_info_sub('Compared data in file ' + Style.DIM + cfile + Style.RESET_ALL, True)
            ret.append(cfile)
        else:
            stdout.print_error('Compared data file ' + Style.DIM + cfile + Style.RESET_ALL + ' does not exist')
            has_error = True
    
    # `with` file
    if options['action'] == 'compare_self':
        # When it is not specified, e. g. the action is parsed as 'compare_self', do nothing
        if not has_error: stdout.print_info_sub('Comparing orbits with each other', True)
        ret.append(None)
    elif 'with' in options['data']:
        # When a 'with' parameter is specified for any other action
        if options['data']['with'] == 'default':
            # When it is set to default, use the built-in database
            if not has_error: stdout.print_info_sub('Comparing with built-in meteor shower orbit database')
            ret.append(path.join(path.dirname(path.realpath(__file__)), '../constants/showers.tsv'))
        else:
            # When it is any other string, check that it exists
            wfile = path.abspath(options['data']['with'])
            if path.exists(wfile):
                if not has_error: stdout.print_info_sub('Comparing with file ' + Style.DIM + wfile + Style.RESET_ALL, True)
                ret.append(wfile)
            else:
                stdout.print_error('File to be comapred with ' + Style.DIM + wfile + Style.RESET_ALL + ' does not exist')
                has_error = True
    else:
        # When it is not specified for any other action (which should not occur), fail
        stdout.print_error('File to compare with not specified')
        has_error = True

    if has_error: raise ValueError('Input files not properly specified')
    return ret


_refstream = None
_refiter = None
_reflock = threading.Lock()
def get_reference_file(path: str):
    """Thread-safe open the reference (`data_with`) file and return a TSV iterator."""
    global _refstream, _refiter
    _reflock.acquire()
    if _refiter is None:
        _refstream = open(path, 'r', encoding='utf8')
        _refiter = csv.reader(_refstream, delimiter='\t')
    _reflock.release()
    return _refiter

def release_reference_file():
    """Thread-safe destroy the reference file iterator and close the stream."""
    global _refstream, _refiter
    _reflock.acquire()
    _refiter = None
    if not _refstream is None: _refstream.close()
    _refstream = None
    _reflock.release()

_comstream = None
def get_compared_file(path: str):
    """Open the compared (`data_compare`) file and return a TSV iterator."""
    global _comstream
    _comstream = open(path, 'r', encoding='utf8')
    return csv.reader(_comstream, delimiter='\t')

def realease_compared_file():
    """Close the compared file stream."""
    global _comstream
    if not _comstream is None: _comstream.close()
    _comstream = None
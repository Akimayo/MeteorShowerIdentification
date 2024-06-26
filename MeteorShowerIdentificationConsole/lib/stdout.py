"""
Provides utilities for writing formatted output to console.
"""
#file -- meta/stdout.py --
from colorama import Fore, Back, Style, Cursor
import threading
from tempfile import _TemporaryFileWrapper

_use_verbose = False
def use_verbose():
    global _use_verbose
    _use_verbose = True

#region Definitions
_TSTAT_MAIN = '╠══'
_TSTAT_MAIN_BRANCH = '╠╤═'
_TSTAT_CON = '║'
_TSTAT_CON_ALONE = '╟'
_TSTAT_SUB = '├─╴'
_TSTAT_SUB_END = '└─╴'
_TSTAT_SUB_ALONE = '──╴'

def _mkstat_main(fore: str, back: str, name: str, ml: bool) -> str: return Fore.BLACK + back + (_TSTAT_MAIN_BRANCH if ml else _TSTAT_MAIN) + Back.RESET + fore + ' ' + name + ':' + Fore.RESET + ' '
def _mkstat_sub(fore: str, back: str, ml: bool) -> str: return Fore.BLACK + back + _TSTAT_CON + Back.RESET + fore + (_TSTAT_SUB if ml else _TSTAT_SUB_END) + Fore.RESET + ' '
def _mkstat_alone(fore: str, back: str) -> str: return Fore.BLACK + back + _TSTAT_CON_ALONE   + Back.RESET + fore  + _TSTAT_SUB_ALONE + Fore.RESET + ' '

_STAT = {}
for type in [
    {'name': 'info', 'fore': Fore.BLUE, 'back': Back.LIGHTBLUE_EX},
    {'name': 'warn', 'fore': Fore.YELLOW, 'back': Back.LIGHTYELLOW_EX},
    {'name': 'error', 'fore': Fore.RED, 'back': Back.LIGHTRED_EX},
    {'name': 'success', 'fore': Fore.GREEN, 'back': Back.LIGHTGREEN_EX},
    {'name': 'working', 'fore': Fore.CYAN, 'back': Back.LIGHTCYAN_EX}
    ]:
    _STAT[type['name']] = [
        _mkstat_main(type['fore'], type['back'], type['name'], False),
        _mkstat_main(type['fore'], type['back'], type['name'], True),
        _mkstat_sub(type['fore'], type['back'], False),
        _mkstat_sub(type['fore'], type['back'], True),
        _mkstat_alone(type['fore'], type['back'])
    ]

_last_sub = None
_last_main = None
_lock = threading.Lock()


def _generic_print_all(type: str, text: str, more: list[str]):
    global _last_sub, _last_main, _lock
    _lock.acquire()
    print((_STAT[type][1] if len(more) > 0 else _STAT[type][0]) + text + '  ')
    if len(more) > 0:
        for line in more[:-1]:
            print(_STAT[type][3] + str(line) + '  ')
        print(_STAT[type][2] + str(more[-1]) + '  ')
        _last_main = None
        _last_sub = type
    else:
        _last_main = type
        _last_sub = None
    _lock.release()
def _generic_print(type: str, text: str):
    global _last_main, _last_sub, _lock
    _lock.acquire()
    print(_STAT[type][0] + text + '  ')
    _last_main = type
    _last_sub = None
    _lock.release()
def _generic_print_sub(type: str, text: str, verbose: bool):
    global _last_main, _last_sub, _use_verbose, _lock
    if verbose and not _use_verbose: return
    _lock.acquire()
    if _last_main == type:
        print(Cursor.UP() + _STAT[type][1])
        print(_STAT[type][2] + text + '  ')
        _last_sub = type
    elif _last_sub == type:
        print(Cursor.UP() + _STAT[type][3])
        print(_STAT[type][2] + text + '  ')
        _last_sub = type
    else:
        print(_STAT[type][4] + text + '  ')
        _last_sub = None
    _last_main = None
    _lock.release()
#endregion

def print_info_all(text: str, more: list[str] = []):
    """Print multi-line informaition."""
    _generic_print_all('info', text, more)
def print_info(text: str):
    """Print single-line information."""
    _generic_print('info', text)
def print_info_sub(text: str, verbose: bool = False):
    """Print single-line additional information and attach it to previous information line."""
    _generic_print_sub('info', text, verbose)

def print_warn_all(text: str, more: list[str] = []):
    """Print a multi-line warning."""
    _generic_print_all('warn', text, more)
def print_warn(text: str):
    """Print a single-line warning."""
    _generic_print('warn', text)
def print_warn_sub(text: str, verbose: bool = False):
    """Print single-line warning details and attach them to previous warning line."""
    _generic_print_sub('warn', text, verbose)

def print_error_all(text: str, more: list[str] = []):
    """Print a multi-line error message."""
    _generic_print_all('error', text, more)
def print_error(text: str):
    """Print a single-line error message."""
    _generic_print('error', text)
def print_error_sub(text: str, verbose: bool = False):
    """Print single-line error details and attach them to previous error line."""
    _generic_print_sub('error', text, verbose)

def print_success_all(text: str, more: list[str] = []):
    """Print a multi-line success message."""
    _generic_print_all('success', text, more)
def print_success(text: str):
    """Print a single-line success message."""
    _generic_print('success', text)
def print_success_sub(text: str, verbose: bool = False):
    """Print a single-line success details and attach them to previous success line."""
    _generic_print_sub('success', text, verbose)

def print_working(text: str):
    """Print a single-line working status."""
    _generic_print('working', text)
def print_working_sub(text: str, verbose: bool = True):
    """Print a single-line working status. WARNING: This method, unlike other statuses, defaults to verbose-only!"""
    _generic_print_sub('working', text, verbose)

def print_config(name: str, config: dict = {}):
    """Print information about loaded configuration file."""
    if _use_verbose:
        print_info_all('Using config file ' + Fore.LIGHTBLACK_EX + name + Fore.RESET,
                       [Style.DIM + config.__str__() + Style.RESET_ALL])
    else:
        print_info_all('Using config file ' + Fore.LIGHTBLACK_EX + name + Fore.RESET)

def print_result(stream: _TemporaryFileWrapper):
    for l in stream:
        print(Back.GREEN + Fore.BLACK + _TSTAT_CON + Fore.RESET + Back.RESET + ' ' + l[:-1])

_LOADER_FRAMES = '🌑🌒🌓🌔🌕🌖🌗🌘'
_LOADER_FRAME_COUNT = len(_LOADER_FRAMES)
class progress:
    """Provides state for a progress animation."""
    # This uses the ASCII escape codes for changing position in the console to keep writing on the same line
    def __init__(self, message: str):
        """Define a new progress animation."""
        self.message = message
        self.i = 0
        self._print_full()

    def _print_full(self):
        global _last_main, _last_sub, _lock
        line = Back.CYAN + Fore.BLACK + _TSTAT_CON + Back.RESET + Fore.RESET + _LOADER_FRAMES[self.i] + '  ' + self.message 
        _lock.acquire()
        print(line + Cursor.BACK(len(line)) + Cursor.UP(1))
        # _last_main = None  # This was used to reset the connectors, but it was messing up connectors in error messages
        # _last_sub = None   # and unnecessarily disconnecting related mesasges, so it's turned off.
        _lock.release()

    def animate(self, count: int = 0):
        """Step forward in the progress animation and print the line."""
        global _last_main, _last_sub, _lock
        self.i = (self.i + 1) % _LOADER_FRAME_COUNT
        # if _last_main is None and _last_sub is None:                        # This was used in conjunction with the resets in `_print_full()`, but those
        #     if count > 0:                                                   # were disabled, so now this just always prints the entire loading message,
        #         if count < 10: msg = _LOADER_FRAMES[self.i] + str(count)    # which turns out to not be a big deal.
        #         else: msg = _LOADER_FRAMES[self.i] + '+'                    # It hides the thread count, but it actually looks better without it.
        #     else: msg = _LOADER_FRAMES[self.i] + ' '
        #     _lock.acquire()
        #     print(Cursor.FORWARD(1) + msg + Cursor.UP(1) + Cursor.BACK(3))
        #     _lock.release()
        # else: self._print_full()
        self._print_full()

    def end(self, message: str|None = None):
        """Turn the progress line into a `working`-type message."""
        global _lock
        _lock.acquire()
        print(Cursor.UP(1))
        _lock.release()
        print_working_sub(message or self.message, False) # TODO: Maybe end properly?
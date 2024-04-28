from core import ast
from .io import FileStream
from csv import DictReader, Sniffer
import re
from collections.abc import Sequence, Callable, Iterable
from typing import Any
from threading import Lock
from functools import reduce

type ParserFieldName = str|int
type OrbitRef = dict[ParserFieldName, Any]
class ParserOptions:
    """Keeps structured column definitions for the input parsers."""
    def __init__(self):
        self.uses_q = True
        self.uses_name = False
        self.uses_code = False
    def set_name(self, name: ParserFieldName):
        self.name_field = name
        self.uses_name = True
        return self
    def set_code(self, code: ParserFieldName):
        self.code_field = code
        self.uses_code = True
        return self
    def set_perihelion_distance(self, perihelion_distance: ParserFieldName):
        self.perihelion_distance_field = perihelion_distance
        self.uses_q = True
        return self
    def set_semimajor_axis_length(self, semimajor_axis_length: ParserFieldName):
        self.semimajor_axis_length_field = semimajor_axis_length
        self.uses_q = False
        return self
    def set_eccentricity(self, eccentricity: ParserFieldName):
        self.eccentricity_field = eccentricity
        return self
    def set_inclination(self, inclination: ParserFieldName):
        self.inclination_field = inclination
        return self
    def set_asc_node_longitude(self, asc_node_longitude: ParserFieldName):
        self.asc_node_longitude_field = asc_node_longitude
        return self
    def set_perihelion_argument(self, perihelion_argument: ParserFieldName):
        self.perihelion_argument_field = perihelion_argument
        return self
    def __str__(self) -> str:
        s = ''
        if self.uses_code: s += '[code]=' + str(self.code_field) + ', '
        if self.uses_name: s += '[name]=' + str(self.name_field) + ', '
        if self.uses_q: s += '[q]=' + str(self.perihelion_distance_field)
        else: s += '[a]=' + str(self.semimajor_axis_length_field)
        return s + f', [e]={str(self.eccentricity_field)}, [ω]={str(self.perihelion_argument_field)}, [Ω]={str(self.asc_node_longitude_field)}, [i]={str(self.inclination_field)}'

# Column definitions used for the built-in `SHOWERS.tsv` file
DEFAULT_DATASET_PARSER_OPTIONS = (ParserOptions().set_code('code')
                                                 .set_name('name')
                                                 .set_perihelion_distance('q')
                                                 .set_eccentricity('e')
                                                 .set_perihelion_argument('peri')
                                                 .set_asc_node_longitude('node')
                                                 .set_inclination('i'))
# Column definitions used as fallback for manually set input files
FALLBACK_PARSER_OPTIONS = (ParserOptions().set_code('CODE')
                                          .set_perihelion_distance('PERIH')
                                          .set_eccentricity('ECC')
                                          .set_perihelion_argument('ARGUP')
                                          .set_inclination('INCL')
                                          .set_asc_node_longitude('NODE'))

type ParserMethod = Callable[[OrbitRef],ast.Orbit]
class Parser(Iterable):
    """Class for thread-safe reading and parsing of orbits. This is an abstract definition -- use `CsvParser` or `DatParser` instead."""
    _lock = Lock()
    def __init__(self, stream: FileStream, options: ParserOptions):
        """Initialize a parser."""
        self.stream = stream
        self.fieldnames = None
        # Initialize lambdas for turning dictionaries from input file lines into `Orbit` instances.
        pre_creator: ParserMethod = (lambda ref: ast.Orbit.from_q(
            float(ref[options.perihelion_distance_field]),
            float(ref[options.eccentricity_field]),
            float(ref[options.inclination_field]),
            float(ref[options.perihelion_argument_field]),
            float(ref[options.asc_node_longitude_field])
        )) if options.uses_q else (lambda ref: ast.Orbit.from_a(
            float(ref[options.semimajor_axis_length_field]),
            float(ref[options.eccentricity_field]),
            float(ref[options.inclination_field]),
            float(ref[options.perihelion_argument_field]),
            float(ref[options.asc_node_longitude_field])
        ))
        if options.uses_name:
            if options.uses_code: self.creator: ParserMethod = lambda ref: pre_creator(ref).with_name(f'[{ref[options.code_field]}] {ref[options.name_field]}')
            else: self.creator: ParserMethod = lambda ref: pre_creator(ref).with_name(ref[options.name_field])
        elif options.uses_code: self.creator: ParserMethod = lambda ref: pre_creator(ref).with_name(ref[options.code_field])
        else: self.creator: ParserMethod = pre_creator
    def __iter__(self):
        return self
    def __next__(self) -> ast.Orbit:
        raise StopIteration() # Abstract implementation, end immediately.
    def get_fieldnames(self) -> Sequence[str]|None:
        """Get the fieldnames available in the current input."""
        return self.fieldnames
    def top(self):
        """Reset the reader to the beginning of the data."""
        self.stream.seek(0) # Abstract implementation, seeking to zero is usually not wanted

class DatParser(Parser):
    HEADER_PATTERN = r'(([\w\s]+?)\s{2,})' # Checks the header line and retrieves column names and positions if possible
    NO_HEADER_PATTERN = r'((.+?)\s{2,})' # Only checks the header line and saves column positions
    def __init__(self, stream: FileStream, options: ParserOptions):
        super().__init__(stream, options)
        self.fields: list[tuple[int,int,ParserFieldName]] = [] # Holds column start position, column end position, and column name
        self.ref: OrbitRef = {}
        self.fieldnames: Sequence[ParserFieldName] = []
        first_line = stream.readline()
        if re.match(self.HEADER_PATTERN, first_line):
            # First line is header row -> Save column names and positions and set data start to next line
            self._data_start = stream.tell()
            for colname in re.finditer(self.HEADER_PATTERN, first_line):
                self.fieldnames.append(colname.group(2))
                self.fields.append((colname.start(), colname.end(), colname.group(2)))
        else:
            # First line is already data -> Save column positions and set data start to start of file
            self._data_start = 0
            i = 0
            for colname in re.finditer(self.NO_HEADER_PATTERN, first_line):
                self.fieldnames.append(i)
                self.fields.append((colname.start(), colname.end(), i))
                i += 1
            stream.seek(0)
    def __next__(self):
        self._lock.acquire()
        line = self.stream.readline()
        self._lock.release()
        if not line: raise StopIteration()
        l = len(line)
        for f in self.fields:
            # Very carefully gets data from columns
            if f[0] > l: self.ref[f[2]] = None # When line is shorter than start of field, set field to None
            elif f[1] > l: self.ref[f[2]] = line[f[0]:].strip() # When line s shorter than end of field, use the rest of the line as field value
            else: self.ref[f[2]] = line[f[0]:f[1]].strip() # If the line is as expected, use the proper column range as field value
        return self.creator(self.ref)
    def top(self):
        self.stream.seek(self._data_start)
        
class CsvParser(Parser):
    def __init__(self, stream: FileStream, options: ParserOptions):
        super().__init__(stream, options)
        dialect = Sniffer().sniff(stream.read(1024))
        stream.seek(0)
        self.parser = DictReader(stream, dialect=dialect)
        self.fieldnames = self.parser.fieldnames
        # Hack to find start of data (can't use `tell()` because `DictReader` uses `__next__()`, which disables `tell()`)
        self._data_start = reduce(lambda sum, name: sum + len(name) + 1, self.fieldnames, 0) + 1 if self.fieldnames else 0
    def __next__(self):
        self._lock.acquire()
        try: ref = self.parser.__next__() # Let `StopIteration` and other exceptions bubble up...
        finally: self._lock.release()     # ...but always make sure to release the lock.
        return self.creator(ref)
    def top(self):
        self.stream.seek(self._data_start)
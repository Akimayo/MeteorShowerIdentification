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

DEFAULT_DATASET_PARSER_OPTIONS = (ParserOptions().set_code('code')
                                                 .set_name('name')
                                                 .set_perihelion_distance('q')
                                                 .set_eccentricity('e')
                                                 .set_perihelion_argument('peri')
                                                 .set_asc_node_longitude('node')
                                                 .set_inclination('i'))
FALLBACK_PARSER_OPTIONS = (ParserOptions().set_code('CODE')
                                          .set_perihelion_distance('PERIH')
                                          .set_eccentricity('ECC')
                                          .set_perihelion_argument('ARGUP')
                                          .set_inclination('INCL')
                                          .set_asc_node_longitude('NODE'))

type ParserMethod = Callable[[OrbitRef],ast.Orbit]
class Parser(Iterable):
    _lock = Lock()
    def __init__(self, stream: FileStream, options: ParserOptions):
        self.stream = stream
        self.fieldnames = None
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
        raise StopIteration()
    def get_fieldnames(self) -> Sequence[str]|None:
        return self.fieldnames
    def top(self):
        self.stream.seek(0)

class DatParser(Parser):
    HEADER_PATTERN = r'(([\w\s]+?)\s{2,})'
    NO_HEADER_PATTERN = r'((.+?)\s{2,})'
    def __init__(self, stream: FileStream, options: ParserOptions):
        super().__init__(stream, options)
        self.fields: list[tuple[int,int,ParserFieldName]] = []
        self.ref: OrbitRef = {}
        self.fieldnames: Sequence[ParserFieldName] = []
        first_line = stream.readline()
        if re.match(self.HEADER_PATTERN, first_line):
            self._data_start = stream.tell()
            for colname in re.finditer(self.HEADER_PATTERN, first_line):
                self.fieldnames.append(colname.group(2))
                self.fields.append((colname.start(), colname.end(), colname.group(2)))
        else:
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
            if f[0] > l: self.ref[f[2]] = None
            elif f[1] > l: self.ref[f[2]] = line[f[0]:].strip()
            else: self.ref[f[2]] = line[f[0]:f[1]].strip()
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
        self._data_start = reduce(lambda sum, name: sum + len(name) + 1, self.fieldnames, 0) + 1 if self.fieldnames else 0
    def __next__(self):
        self._lock.acquire()
        try: ref = self.parser.__next__()
        finally: self._lock.release()
        return self.creator(ref)
    def top(self):
        self.stream.seek(self._data_start)
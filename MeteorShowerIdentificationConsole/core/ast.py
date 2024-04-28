"""
Data structures for representing orbits and results of comparison.
"""

from math import pi
from threading import Lock
from math import sqrt

class Orbit:
    def __init__(self, q: float, e: float, i: float, w: float, o: float):
        if q <= 0: raise ValueError('Perihelion distance should be positive', q)
        self.q = q
        self._a = None

        if e < 0: raise ValueError('Eccentricity cannot be negative', e)
        # if e > 1: raise ValueError('Eccentricity gives a hyperbolic orbit', e) # TODO: Should we check eccentricity greater than one? It could be a hyperbolic orbit 
        self.e = e

        self.i = i / 180 * pi

        self.w = w / 180 * pi

        self.o = o / 180 * pi

        self.name = None


    def __str__(self) -> str:
        return (
            ((self.name + ' ') if self.name else '') +
            f'[q={round(self.q, 3)}AU|e={round(self.e, 3)}|i={round(self.i / pi * 180, 3)}°|ω={round(self.w / pi * 180, 3)}°|Ω={round(self.o / pi * 180, 3)}°]'
        )

    def with_name(self, name: str):
        """Set the orbit name."""
        self.name = name
        return self
    
    def _get_a(self) -> float:
        if self._a is None:
            self._a = self.q / (1 - self.e)
        return self._a
    def _set_a(self, value: float):
        self._a = value
        self.q = value * (1 - self.e)
    a = property(_get_a, _set_a)

    @staticmethod
    def a_to_q(a: float, e: float) -> float:
        """Convert semimajor axis length `a` to perihelion distance `q` using eccentricity `e`."""
        return a * (1 - e)

    @classmethod
    def from_a(cls, a: float, e: float, i: float, w: float, o: float):
        """Create an `Orbit` instance from semimajor axis length `a`."""
        return cls(
            cls.a_to_q(a, e),
            e, i, w, o
        )

    @classmethod
    def from_q(cls, q: float, e: float, i: float, w: float, o: float):
        """Create an `Orbit` instance from perihelion distance `q`."""
        return cls(q, e, i, w, o)

class CriterionResolution:
    def __init__(self, crit: str, d2_value: float, d_cutoff: float) -> None:
        self.criterion = crit
        self.d2 = d2_value
        self.limit = d_cutoff
        limit2 = d_cutoff * d_cutoff
        self.quality = d2_value / limit2
        self.success = d2_value < limit2
        pass
    def __lt__(self, value: object) -> bool:
        if isinstance(value, CriterionResolution): return self.quality < value.quality
        else: raise TypeError()
    def __le__(self, value: object) -> bool:
        if isinstance(value, CriterionResolution): return self.quality <= value.quality
        else: raise TypeError()
    def __eq__(self, value: object) -> bool:
        if isinstance(value, CriterionResolution): return self.criterion == value.criterion and self.d2 == value.d2 and self.limit == value.limit
        else: return False
    def __ge__(self, value: object) -> bool:
        if isinstance(value, CriterionResolution): return self.quality >= value.quality
        else: raise TypeError()
    def __gt__(self, value: object) -> bool:
        if isinstance(value, CriterionResolution): return self.quality > value.quality
        else: raise TypeError()
    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)
    def __str__(self) -> str:
        return f'D({self.criterion})={round(sqrt(self.d2), 3)} (cutoff {round(self.limit, 3)})'

class _Output:
    def __init__(self, name: str) -> None:
        self._HEADER = f'***** {self.__class__.__name__} {name} *****\n'
        self.HEADER_LENGTH = len(self._HEADER)
    def _serialize(self) -> str:
        return ''
    def __str__(self) -> str:
        return self._HEADER + self._serialize()

_result_lock = Lock()
class Result(_Output):
    def __init__(self, orbit: Orbit) -> None:
        super().__init__(orbit.name or str(orbit))
        self.accepted: dict[str,list[CriterionResolution]] = {}
        self.rejected: list[tuple[str,CriterionResolution]|None] = [None,None,None]
        self.orbit = orbit
        

    def __setitem__(self, __name: str, __value: CriterionResolution) -> None:
        if __value.limit < 0: return # Disregard mathematical rejections
        if __value.success: # When criterion is met
            if not __name in self.accepted: self.accepted[__name] = []
            self.accepted[__name].append(__value)
            return
        # Store rejections ordered by match quality
        _result_lock.acquire()
        if self.rejected[0] is None or __value < self.rejected[0][1]:
            self.rejected[2] = self.rejected[1]
            self.rejected[1] = self.rejected[0]
            self.rejected[0] = (__name, __value)
        elif self.rejected[1] is None or __value < self.rejected[1][1]:
            self.rejected[2] = self.rejected[1]
            self.rejected[1] = (__name, __value)
        elif self.rejected[2] is None or __value < self.rejected[2][1]:
            self.rejected[2] = (__name, __value)
        _result_lock.release()

    def _serialize(self) -> str:
        accepted = '\n'.join(
            map(lambda p: '✔️\t' + p[0] + '\t' + '\t'.join(
                map(lambda c: str(c), p[1])
            ), sorted(self.accepted.items(), key=lambda p: min(p[1])))
            )
        rejected = '\n'.join(map(lambda p: '✖️\t' + p[0] + '\t' + str(p[1]), filter(lambda p: not p is None, self.rejected))) # type: ignore
        return (rejected if not accepted else accepted + '\n' + rejected) + '\n'

class Shower(_Output):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.orbits = [name]
    
    def _serialize(self) -> str:
        return '\n'.join(self.orbits) + '\n'
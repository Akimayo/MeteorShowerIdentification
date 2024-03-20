from math import pi
from typing import Any

CriterionResolution = tuple[str,float,bool,float]

class Orbit:
    def __init__(self, q: float, e: float, i: float, w: float, o: float):
        if q <= 0: raise ValueError('Perihelion distance should be positive', q)
        self.q = q

        if e < 0: raise ValueError('Eccentricity cannot be negative', e)
        if e > 1: raise ValueError('Eccentricity gives a hyperbolic orbit', e) # TODO: Should we check eccentricity greater than one? It could be a hyperbolic orbit 
        self.e = e

        self.i = i / 180 * pi

        self.w = w / 180 * pi

        self.o = o / 180 * pi

        self.name = None


    def __str__(self) -> str:
        return (
            ((self.name + ' ') if self.name is str else '') +
            f'[q={round(self.q, 3)}AU|e={round(self.e, 3)}|i={round(self.i / pi * 180, 3)}°|ω={round(self.w / pi * 180, 3)}°|Ω={round(self.o / pi * 180, 3)}°]'
        )

    def with_name(self, name: str):
        """Set the orbit name."""
        self.name = name
        return self


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

class Result:
    # FIXME: This needs to be rethought completely: keep track of all criteria, print criteria inline, add meteor params somewhere, test which shower has the most criteria satisfactions
    def __init__(self) -> None:
        self.accepted: dict[str,CriterionResolution] = {}
        self.fallback: tuple[str,CriterionResolution]|None = None

    def __setitem__(self, __name: str, __value: CriterionResolution) -> None:
        if __value[2]:
            self.accepted[__name] = __value
        elif self.fallback is None or __value[1] < self.fallback[1][1]:
            self.fallback = (__name, __value)

    def __str__(self) -> str:
        accepted = '\n'.join(map(lambda p: f'{p[0]}\t✅{p[1][0]}\tD={round(p[1][1], 3)} (cutoff {p[1][3]})', sorted(self.accepted.items(), key=lambda p: p[1][1])))
        return (accepted if self.fallback is None else accepted + f'\n{self.fallback[0]}\t✕ {self.fallback[1][0]}\tD={round(self.fallback[1][1], 3)} (cutoff {self.fallback[1][3]})')
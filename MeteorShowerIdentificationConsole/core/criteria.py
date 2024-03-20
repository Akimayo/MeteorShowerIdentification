"""
Provides D-criteria calculation functions
"""

from . import ast
import math

def d_sh(o1: ast.Orbit, o2: ast.Orbit, cutoff: float|None = None) -> ast.CriterionResolution:
    sin_i = 2 * math.sin((o2.i - o1.i)/2)
    sin_o = 2 * math.sin((o2.o - o1.o)/2)
    sin_comb = (o1.e+o2.e) * math.sin((o2.o + o2.w - o1.o - o1.w)/2)
    d2 = (
        (o2.e - o1.e) * (o2.e - o1.e) +
        (o2.q - o1.q) * (o2.q - o1.q) +
        sin_i * sin_i +
        math.sin(o1.i) * math.sin(o2.i) * sin_o * sin_o +
        sin_comb * sin_comb
         )
    d = math.sqrt(d2)
    # return ('sh', d, d2 <= 0.0625, 0.25) # TODO: Better cutoffs for different inclinations
    return ('sh', d, d2 <= 0.09, 0.3)

CRITERIA = {
    'sh': d_sh
}
ALL_CRITERIA = list(CRITERIA.keys())
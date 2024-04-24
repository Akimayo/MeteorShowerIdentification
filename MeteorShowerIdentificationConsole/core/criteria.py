"""
Provides D-criteria calculation functions
"""

from . import ast
import math

def d_sh(o1: ast.Orbit, o2: ast.Orbit, cutoff: float|None = None) -> ast.CriterionResolution:
    """Implementation of the original Southworth-Hawkins dissimilarity measure"""
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
    limit = 0
    if not cutoff is None: limit = cutoff
    elif o1.i < 10 and o2.i < 10: limit = 0.09
    elif o1.i < 90 and o2.i < 90: limit = 0.12
    return ast.CriterionResolution('sh', d2, limit)

def d_d(o1: ast.Orbit, o2: ast.Orbit, cutoff: float|None = None) -> ast.CriterionResolution:
    """Implementation of Drummond's dissimilarity measure"""
    q_over = (o2.q - o1.q) / (o1.q + o2.q)
    e_sum = o1.e + o2.e
    e_over = (o2.e - o1.e) / e_sum
    incl = math.acos(
        math.cos(o1.i) * math.cos(o2.i) +
        math.sin(o1.i) * math.sin(o2.i) * math.cos(o2.o - o1.o)
    ) / math.pi
    sin_b1 = math.sin(o1.i) * math.sin(o1.w)
    b1 = math.asin(sin_b1)
    sin_b2 = math.sin(o2.i) * math.sin(o2.w)
    b2 = math.asin(sin_b2)
    l1 = o1.o + math.atan(math.cos(o1.i) * math.tan(o1.w))
    if math.cos(o1.w) > 0: l1 += math.pi
    l2 = o2.o + math.atan(math.cos(o2.i) * math.tan(o2.w))
    if math.cos(o2.w) > 0: l2 += math.pi
    theta = math.acos(
        sin_b1 * sin_b2 +
        math.cos(b1) * math.cos(b2) * math.cos(l2 - l1)
    ) / math.pi if l2 != l1 else 0
    d2 = (q_over * q_over +
          e_over * e_over +
          incl * incl +
          e_sum * e_sum * theta * theta / 4)
    limit = 0.18
    if not cutoff is None: limit = cutoff
    elif o1.i < 10 and o2.i < 10: limit = 0.09
    elif o1.i < 90 and o2.i < 90: limit = 0.11
    return ast.CriterionResolution('d', d2, limit)

def d_h(o1: ast.Orbit, o2: ast.Orbit, cutoff: float|None = None) -> ast.CriterionResolution:
    """Implementation of Jopek's hybrid dissimilarity measure"""
    sin_i = 2 * math.sin((o2.i - o1.i)/2)
    sin_o = 2 * math.sin((o2.o - o1.o)/2)
    sin_comb = (o1.e+o2.e) * math.sin((o2.o + o2.w - o1.o - o1.w)/2)
    q_over = (o2.q - o1.q) / (o2.q + o1.q)
    d2 = (
        q_over * q_over +
        (o2.e - o1.e) * (o2.e - o1.e) +
        sin_i * sin_i +
        math.sin(o1.i) * math.sin(o2.i) * sin_o * sin_o +
        sin_comb * sin_comb
         )
    d = math.sqrt(d2)
    limit = 0
    if not cutoff is None: limit = cutoff
    elif o1.i < 10 and o2.i < 10: limit = 0.10
    elif o1.i < 90 and o2.i < 90: limit = 0.16
    return ast.CriterionResolution('h', d2, limit)

DN_W1 = 1; DN_W2 = 1; DN_W3 = 1
def d_n(o1: ast.Orbit, o2: ast.Orbit, cutoff: float|None = None) -> ast.CriterionResolution:
    """Implementation of the new approach method by Valsecchi, Jopek and Froeschlé"""
    try:
        ar1 = 1/o1.a
        b1 = o1.a * (1 - o1.e * o1.e)
        t1 = ar1 + 2 * math.sqrt(b1) * math.cos(o1.i)
        u1 = math.sqrt(3 - t1)
        phi1 = math.atan((math.sqrt(2 - ar1 - b1)) / u1)
        ar2 = 1/o2.a
        b2 = o2.a * (1 - o2.e * o2.e)
        t2 = ar2 + 2 * math.sqrt(b2) * math.cos(o2.i)
        u2 = math.sqrt(3 - t2)
        phi2 = math.atan((math.sqrt(2 - ar2 - b2)) / u2)
        ctheta1 = (1 - u1 * u1 - ar1) / (2 * u1)
        ctheta2 = (1 - u2 * u2 - ar2) / (2 * u2)
        du = u2 - u1
        dct = ctheta2 - ctheta1
        _dphi = (phi2 - phi1) / 2
        dphi_i = math.sin(_dphi)
        dphi_ii = math.sin(math.pi / 2 + _dphi)
        dx2 = 2 * min(DN_W2 * dphi_i * dphi_i, DN_W2 * dphi_ii * dphi_ii)
        # TODO: Add delta-lambda to dx2?
    except ZeroDivisionError:
        return ast.CriterionResolution('n', 0, -1) # Parabolic orbits are not really supported
    except ValueError:
        return ast.CriterionResolution('n', 0, -1) # When squre roots are out of bounds
    else:
        d2 = (du * du +
            DN_W1 * (dct * dct) +
            dx2)
        limit = 0
        if not cutoff is None: limit = cutoff
        elif o1.i < 10 and o2.i < 10: limit = 0.08
        elif o2.i < 90 and o2.i < 90: limit = 0.09
        else: limit = 0.17
        return ast.CriterionResolution('n', d2, limit)

CRITERIA = {
    'sh': d_sh,
    'd': d_d,
    'h': d_h,
    'n': d_n
}
ALL_CRITERIA = list(CRITERIA.keys())
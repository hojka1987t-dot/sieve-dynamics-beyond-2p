"""Coefficients l_j of Holt's exact models (Holt 2026, arXiv 2608.26384, eq. 1.2)
for gaps 84..104, from initial conditions in G(47#).

For g <= 104 every step from 47# on is linear (2*53 = 106 > 104), so these initial
conditions give exact models for all later stages. Built-in check: l_1 must equal the
Hardy-Littlewood constant prod_{q | g, q odd} (q-1)/(q-2) (Holt, eq. 1.3).

Usage: python holt_models.py ../../data/nG47.csv
"""
import sys
from fractions import Fraction
from math import prod, comb

from load_ng import load_ng

ODD = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def hl_constant(g):
    c = Fraction(1)
    for q in ODD + [53]:
        if g % q == 0:
            c *= Fraction(q - 1, q - 2)
    return c


def main(path, g_from=84, g_to=104, nterms=4):
    n = load_ng(path)
    M = prod(p - 2 for p in ODD)          # number of gaps 2 in G(47#)
    ok = 0
    print("   g        l_1     HL const   " + "   ".join("l_%d" % j for j in range(2, nterms + 1)))
    for g in range(g_from, g_to + 1, 2):
        w = {j: Fraction(v, M) for j, v in n[g].items()}
        J = max(w)
        l = [sum(comb(i - 1, j - 1) * w.get(i, 0) for i in range(j, J + 1))
             for j in range(1, nterms + 1)]
        good = (l[0] == hl_constant(g))
        ok += good
        print("  %4d  %9.6f  %9.6f  " % (g, float(l[0]), float(hl_constant(g)))
              + "  ".join("%9.4f" % float(x) for x in l[1:])
              + ("   OK" if good else "   MISMATCH"))
    total = (g_to - g_from) // 2 + 1
    print("\nl_1 equal to the Hardy-Littlewood constant (exactly, as fractions): %d/%d" % (ok, total))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../../data/nG47.csv")

"""Reproduces Figure 6 of Holt (arXiv 2608.26384v3): populations of the constellation
s = 2,10,2,10,2 and its driving terms of lengths 5, 6, 7 for p = 5, 7, 11, 13.

The transitions 5->7, 7->11 and 11->13 lie outside Holt's linear model (|s| = 26 >= 2p);
Holt lists them as computed values. Here they are derived from the previous stage by
Theorem 4 (transition law with residue classes) and compared with brute force.

Usage: python holt_fig6.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brute_force"))
from kon import populacje, przewidz   # noqa: E402

s = (2, 10, 2, 10, 2)
C = [0]
for g in s:
    C.append(C[-1] + g)
HOLT = {5: (0, 0, 1), 7: (1, 0, 2), 11: (6, 4, 8), 13: (52, 44, 48)}
stages = [([2, 3, 5], 5), ([2, 3, 5, 7], 7), ([2, 3, 5, 7, 11], 11), ([2, 3, 5, 7, 11, 13], 13)]

p5, _ = populacje([2, 3, 5], C)
print("p=5 : brute force %s, Holt %s" % (tuple(p5.get(j, 0) for j in (5, 6, 7)), HOLT[5]))
for (P, p), (Pn, q) in zip(stages[:-1], stages[1:]):
    _, windows = populacje(P, C)
    pred, multi = przewidz(windows, C, q)
    fact, _ = populacje(Pn, C)
    a = tuple(pred.get(j, 0) for j in (5, 6, 7))
    b = tuple(fact.get(j, 0) for j in (5, 6, 7))
    status = "MATCH" if a == b == HOLT[q] else "DIFFERENT"
    print("p=%-2d: Theorem 4 %s, brute force %s, Holt %s -> %s (multi-point fusions: %d)"
          % (q, a, b, HOLT[q], status, multi))

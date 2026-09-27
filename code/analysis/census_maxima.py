"""How maximal gaps h(n) of G(p_n#) are born.

For each maximal configuration, count the interior points that the largest prime p_n
kills alone (points not covered by the smaller primes):
  |U| = 1  -> born from a pair of adjacent gaps of G(p_{n-1}#),
  |U| = 2  -> born from a triple with middle gap 2p_n ("rescue").
In every rescue the two points are exactly 2p_n apart (checked by the script).

Inputs (third-party, not redistributed here; download from the original sources):
  - Ziller's file of all maximal configurations for n <= 54 (remainders_txt.txt),
  - the OEIS A048670 table with start positions u(n) for n <= 64 (b-file a048670.txt).

Usage: python census_maxima.py remainders_txt.txt [a048670.txt]
"""
import re
import sys
from math import gcd, prod


def primes(n):
    p, x = [], 2
    while len(p) < n:
        if all(x % d for d in p if d * d <= x):
            p.append(x)
        x += 1
    return p


def ziller(path):
    txt = open(path, encoding="latin-1").read().replace("\r", "")
    res, bad = {}, 0
    for b in re.split(r"\n-{20,}\n", txt):
        m = re.search(r"n=(\d+), p_n=(\d+), omega\(n\)=(\d+), n_seq=(\d+)", b)
        pm = re.search(r"primes\s+([\d ]+)", b)
        if not m or not pm:
            continue
        n, pn, om, ns = map(int, m.groups())
        P = list(map(int, pm.group(1).split()))
        conf = [list(map(int, l.split("*")[1].split()))
                for l in b.split("\n") if re.match(r"\s*\d+\s+\d+\s*\*", l)]
        sizes = set()
        for r in conf:
            U = [j for j in range(1, om + 1) if all((j - r[i]) % P[i] for i in range(len(P) - 1))]
            sizes.add(len(U))
            if len(U) == 2 and U[1] - U[0] != P[-1]:     # half-scale distance must be p_n
                bad += 1
        res[n] = {frozenset({1}): "pair", frozenset({2}): "rescue"}.get(frozenset(sizes), "mixed")
    return res, bad


def gerbicz(path):
    P = primes(80)
    res, bad = {}, 0
    for line in open(path):
        if not line.strip() or line.startswith("#"):
            continue
        n, h, u = map(int, line.split()[:3])
        if n < 2:
            continue
        Mm = prod(P[:n - 1])
        x0 = u - 1
        U = [t for t in range(1, h) if gcd(x0 + t, Mm) == 1]
        if len(U) == 2 and U[1] - U[0] != 2 * P[n - 1]:
            bad += 1
        res[n] = {1: "pair", 2: "rescue"}.get(len(U), "|U|=%d" % len(U))
    return res, bad


if __name__ == "__main__":
    Z, bz = ziller(sys.argv[1])
    G, bg = gerbicz(sys.argv[2]) if len(sys.argv) > 2 else ({}, 0)
    for n in sorted(set(Z) | set(G)):
        if n < 14:
            continue
        z, g = Z.get(n, ""), G.get(n, "")
        flag = "" if (not z or not g or z == "mixed" or z == g) else "  <-- INCONSISTENT"
        print("n=%2d  Ziller (all configurations): %-7s  Gerbicz/Bozek (one interval): %-7s%s" % (n, z, g, flag))
    print("\nrescues with distance different from 2p_n: Ziller %d, Gerbicz/Bozek %d" % (bz, bg))

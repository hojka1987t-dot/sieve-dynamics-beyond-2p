"""Szacunek czasu silnika 4.5 dla kolejnych etapow: suma po oknach (polowa dzieki symetrii) 2^N * (liczba fal) * c,
c = 10 ns na (podzbior x fala) na jednym rdzeniu tej maszyny (int64 i wielomodularnie prawie tak samo).
Uzycie: python sufit_45.py [rdzenie] [c_ns]"""
import sys
import numpy as np
from math import prod
P = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
CORES = int(sys.argv[1]) if len(sys.argv) > 1 else 16
c = (float(sys.argv[2]) if len(sys.argv) > 2 else 10.0) * 1e-9
def stats(base_k, g):
    base = P[:base_k]; B = prod(base)
    a = np.ones(B + g + 1, dtype=bool)
    for p in base: a[::p] = False
    cs = np.cumsum(a, dtype=np.int32)
    v = np.flatnonzero(a[:B] & a[g:B + g])
    N = (cs[v + g - 1] - cs[v]).astype(np.int64)
    return float((2.0 ** N).sum()) / 2, int(N.max()), len(v)
# etap p0 i nowe luki, dla ktorych modele Holta z p0 sa wazne (g < 2 * nastepna liczba pierwsza)
targets = [(59, [118, 120]), (61, list(range(122, 133, 2))), (67, list(range(134, 141, 2))), (71, [142, 144]),
           (73, list(range(146, 157, 2))), (79, list(range(158, 165, 2))), (83, list(range(166, 177, 2)))]
for stage, gs in targets:
    K = P.index(stage) + 1
    best = None
    for base_k in (4, 5, 6):
        waves = P[base_k:K]
        tot = 0; nmax = 0; per = []
        for g in gs:
            s, nm, nw = stats(base_k, g)
            t = s * len(waves) * c / CORES; tot += t; nmax = max(nmax, nm); per.append(t)
        if best is None or tot < best[0]:
            best = (tot, P[base_k - 1], nmax, per)
    tot, b, nmax, per = best
    print("%3d#: luki %d-%d  najlepsze kolo %2d#  razem %8.1f h na %d rdzeniach  (najwieksza luka %.1f h, Nmax %d)"
          % (stage, gs[0], gs[-1], b, tot / 3600, CORES, max(per) / 3600, nmax), flush=True)

"""Tabela dlugich okien (rozdzial 9 wersji 3), wiersze 'enumeration': glebokosc d_q(y) z pelnego wyliczenia
wszystkich polozen okna dla N = 11#, 13#, 17# i y do 3000 (co 2)."""
import numpy as np
from collections import Counter
def mapa(pr, q, ymax=3000):
    N = int(np.prod(pr)); Q = N * q
    def cs_dla(M, prs):
        a = np.arange(M + ymax + 2, dtype=np.int64); s = np.ones(a.size, np.int32)
        for p in prs: s[a % p == 0] = 0
        return np.concatenate(([0], np.cumsum(s, dtype=np.int32)))
    csN = cs_dla(N, pr); csQ = cs_dla(Q, pr + [q]); ile = Counter(); g2 = []
    for y in range(2 * q, ymax + 1, 2):
        nN = csN[y + 1:y + 1 + N] - csN[:N]; W = int(nN.min())
        if W == 0: continue
        nQ = csQ[y + 1:y + 1 + Q] - csQ[:Q]; W2 = int(nQ.min())
        d = int((nN[np.nonzero(nQ == W2)[0] % N] - W).min()); ile[d] += 1
        if d >= 2: g2.append(y)
    print(q, dict(sorted(ile.items())), 'glebokosc >= 2 przy y =', g2)
for pr, q in (([2,3,5,7,11], 13), ([2,3,5,7,11,13], 17), ([2,3,5,7,11,13,17], 19)):
    mapa(pr, q)

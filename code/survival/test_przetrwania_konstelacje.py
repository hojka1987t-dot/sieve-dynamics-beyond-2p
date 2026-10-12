"""Tabela konstelacji w rozdziale 6.4 wersji 3: pary i trojki kolejnych luk (rozpietosc <= 40) miedzy liczbami
pierwszymi w [47^2, 10^9] wobec cyklu G(P(z)), z = x^c. Warunki poczatkowe: pelne wyliczenie G(19#);
lancuch Holta od q = 23 (jednolity, bo 2q >= 46 > 40). Wymaga: sito_1e9.npz (sito.py), konst_1e9.npz (sito_konst.py),
weryfikacja_wyczerpujaca.py (funkcje ksztalty, punkty)."""
import sys, os
sys.path.insert(0, os.getcwd())
import numpy as np, math
from collections import defaultdict
from itertools import combinations
from weryfikacja_wyczerpujaca import ksztalty, punkty
N, m19 = ksztalty([2,3,5,7,11,13,17,19], 40)
phi = float(np.prod([p - 1 for p in (2,3,5,7,11,13,17,19)]))
n = defaultdict(lambda: defaultdict(int))
for P, c in m19.items():
    pts = punkty(P); L = pts[-1]; wew = pts[1:-1]; Jp = len(pts) - 1
    for m in (2, 3):
        for ch in combinations(wew, m - 1):
            C = (0,) + ch + (L,); s = tuple(C[i + 1] - C[i] for i in range(m)); n[s][Jp] += c
wzory = sorted(n); Jmax = max(max(d) for d in n.values()); mlen = np.array([len(s) for s in wzory], float)
R = np.zeros((len(wzory), Jmax + 2))
for i, s in enumerate(wzory):
    for Jp, c in n[s].items(): R[i, Jp] = c / phi
mm = np.ones(260001, bool); mm[:2] = False
for i in range(2, 510):
    if mm[i]: mm[i*i::i] = False
Q = np.nonzero(mm)[0]; Q = Q[Q >= 23]; Jv = np.arange(Jmax + 2, dtype=float)
etapy = [19]; rs = [R[np.arange(len(wzory)), mlen.astype(int)].copy()]
for q in Q:
    q = float(q); Rn = np.zeros_like(R); Rn[:, :-1] = R[:, 1:]
    R = ((q - Jv - 1) * R + (Jv + 1 - mlen[:, None]) * Rn) / (q - 1)
    etapy.append(int(q)); rs.append(R[np.arange(len(wzory)), mlen.astype(int)].copy())
etapy = np.array(etapy); rs = np.array(rs)
d = np.load('sito_1e9.npz'); Pk = d['P']; ile = d['ile']; k47 = int(np.nonzero(Pk == 47)[0][0])
x = Pk[k47:].astype(float) ** 2; w = ile[k47:].astype(float)
kk = np.load('konst_1e9.npz'); k2 = dict(map(tuple, kk['A2'])); k3 = dict(map(tuple, kk['A3']))
klucz = lambda s: (s[0]//2)*32 + s[1]//2 if len(s) == 2 else (s[0]//2)*1024 + (s[1]//2)*32 + s[2]//2
A = np.array([float((k2 if len(s) == 2 else k3).get(klucz(s), 0)) for s in wzory])
for c in (0.5, 0.55, 0.56, math.exp(-0.5772156649015329), 0.565, 0.57):
    idx = np.clip(np.searchsorted(etapy, x ** c, side='right') - 1, 0, len(etapy) - 1)
    E = (w[:, None] * rs[idx]).sum(axis=0); wyn = []
    for m in (2, 3):
        sel = (mlen == m) & (E > 0); Em = E[sel] * A[sel].sum() / E[sel].sum(); Am = A[sel]
        wyn.append('%.2f%% %.1f' % (np.median(np.abs(Am - Em) / Em) * 100, ((Am - Em) ** 2 / Em).sum() / (sel.sum() - 1)))
    print('%.4f  pary: %s  trojki: %s' % (c, wyn[0], wyn[1]))

"""Akapit 'Statistics' w rozdziale 6.4 wersji 3: rozrzut licznosci kazdej luki w kazdym przedziale przetrwania osobno
wokol modelu, sum (A-E)^2/E / (liczba komorek - 1) po komorkach przedzial x luka z E >= 5.
Wymaga: sito_1e9.npz (sito.py), nG47.csv. Wynik w wersji 3: 0.90 przy c = e^-gamma, 8.37 przy c = 1/2; 140 730 komorek."""
import numpy as np, csv, math
np.seterr(divide='ignore', invalid='ignore')   # komorki z E = 0 sa i tak pomijane (sel)

def _dane(nazwa, *podfoldery):
    """Plik danych: najpierw w biezacym folderze, potem w data/ archiwum (uruchamianie z code/<folder>)."""
    import os
    for p in (nazwa, os.path.join('..', '..', 'data', *podfoldery, nazwa)):
        if os.path.exists(p):
            return p
    return nazwa

d = np.load('sito_1e9.npz'); P = d['P']; cnt = d['cnt']; ile = d['ile']
m = np.ones(400001, bool); m[:2] = False
for i in range(2, 633):
    if m[i]: m[i*i::i] = False
Q = np.nonzero(m)[0]
n = {}
with open(_dane('nG47.csv'), encoding='utf-8') as f:
    for r in csv.reader(f):
        if r and r[0].startswith('Gap Sum'):
            g = int(r[0].split('=')[1]); n[g] = [float(v) if v.strip() else 0.0 for v in r[2:]]
Jm = max(len(v) for v in n.values()); gs = sorted(n)
phi = float(np.prod([float(p - 1) for p in Q[Q <= 47]]))
R = np.array([v + [0.0] * (Jm - len(v)) for v in (n[g] for g in gs)]) / phi; J = np.arange(1, Jm + 1, dtype=float)
i47 = int(np.nonzero(Q == 47)[0][0]); r1 = [R[:, 0].copy()]; kl = [47]
for q in Q[i47 + 1:]:
    q = float(q); Rn = np.zeros_like(R); Rn[:, :-1] = R[:, 1:]; R = ((q - J - 1) * R + J * Rn) / (q - 1); r1.append(R[:, 0].copy()); kl.append(int(q))
r1 = np.array(r1); kl = np.array(kl)
k47 = int(np.nonzero(P == 47)[0][0]); K = len(P)
x = P[k47:K].astype(float) ** 2; w = ile[k47:K].astype(float)
A = np.array([cnt[k47:K, g // 2] for g in gs]).T.astype(float)
for nazwa, c in (('c = 1/2', 0.5), ('c = e^-gamma', math.exp(-0.5772156649015329))):
    idx = np.clip(np.searchsorted(kl, x ** c, side='right') - 1, 0, len(kl) - 1)
    E = w[:, None] * r1[idx]; E *= A.sum() / E.sum(); sel = E >= 5
    print('%s: rozrzut %.3f na %d komorkach (przedzialy: %d)' % (nazwa, ((A - E) ** 2 / E)[sel].sum() / (sel.sum() - 1), int(sel.sum()), K - k47))

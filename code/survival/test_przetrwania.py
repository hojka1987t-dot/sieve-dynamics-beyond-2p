"""Tabela 'survival' (rozdzial 6.4 wersji 3): przerwy 2 <= g <= 104 miedzy liczbami pierwszymi w [47^2, 10^9]
wobec cyklu G(P(z)) na etapie z = x^c, x = p_k^2. Wymaga: sito_1e9.npz (z sito.py) i nG47.csv."""
import numpy as np, csv, math

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
for r in csv.reader(open(_dane('nG47.csv'))):
    if r and r[0].startswith('Gap Sum'):
        g = int(r[0].split('=')[1]); n[g] = [float(v) if v.strip() else 0.0 for v in r[2:]]
Jm = max(len(v) for v in n.values()); gs = sorted(n)
phi = float(np.prod([float(p - 1) for p in Q[Q <= 47]]))
R = np.array([v + [0.0] * (Jm - len(v)) for v in (n[g] for g in gs)]) / phi
J = np.arange(1, Jm + 1, dtype=float)
i47 = int(np.nonzero(Q == 47)[0][0]); r1 = [R[:, 0].copy()]; kl = [47]
for q in Q[i47 + 1:]:                       # lancuch Holta, dokladny dla g <= 104 i q >= 53
    q = float(q); Rn = np.zeros_like(R); Rn[:, :-1] = R[:, 1:]
    R = ((q - J - 1) * R + J * Rn) / (q - 1); r1.append(R[:, 0].copy()); kl.append(int(q))
r1 = np.array(r1); kl = np.array(kl)
k47 = int(np.nonzero(P == 47)[0][0]); K = len(P)
A = np.array([cnt[k47:, g // 2].sum() for g in gs], float)
x = P[k47:K].astype(float) ** 2; w = ile[k47:K].astype(float)
print(' c        mediana |A-E|/E    chi2/stopien swobody')
for c in (0.50, 0.53, 0.55, 0.555, 0.56, math.exp(-0.5772156649015329), 0.565, 0.57, 0.58, 0.60):
    idx = np.clip(np.searchsorted(kl, x ** c, side='right') - 1, 0, len(kl) - 1)
    E = (w[:, None] * r1[idx]).sum(axis=0); E *= A.sum() / E.sum()
    print(f' {c:.4f}   {np.median(np.abs(A - E) / E) * 100:8.3f}%   {((A - E) ** 2 / E).sum() / (len(gs) - 1):14.1f}')

"""Test przetrwania dla par i trojek kolejnych luk o rozpietosci <= 104 (rozszerzenie Tabeli 4 wersji 3, ktora siegala 40).
Warunki poczatkowe: dokladne populacje n_{s,J}(47#) (nK47_konstelacje.csv); lancuch Holta od q = 53 (jednolity, 2q >= 106 > 104).
Licznosci: konst104_1e9.npz (sito_konst104.py). Statystyki jak w wersji 3: dla kazdej konstelacji A = laczna liczba
w [47^2, 10^9], E = suma po przedzialach przetrwania (liczba przerw w przedziale x udzial w cyklu na etapie x^c);
E normalizowane do sumy A osobno dla par i trojek; mediana |A-E|/E i chi^2 na stopien swobody."""
import csv, math, os, numpy as np
from _wspolne import ROOT, DATA
nK = {}
for r in csv.reader(open(os.path.join(DATA, 'pairs_triples', 'nK47_constellations.csv'), encoding='utf-8')):
    s = tuple(int(x) for x in r[0].split('=')[1].split(',')); nK[s] = [int(c) for c in r[2:]]
wz = sorted(nK); Jm = max(len(v) for v in nK.values()) + 2; mlen = np.array([len(s) for s in wz], float)
phi = float(np.prod([p - 1 for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47)]))
R = np.zeros((len(wz), Jm))
for i, s in enumerate(wz):
    for j, c in enumerate(nK[s]): R[i, j + 1] = c / phi           # kolumna J = dlugosc
SITO = next(f for f in ('sito_1e9.npz', os.path.join(ROOT, 'code', 'survival', 'sito_1e9.npz')) if os.path.exists(f))  # z code/survival/sito.py
d = np.load(SITO); Pk = d['P']; ile = d['ile']; k47 = int(np.nonzero(Pk == 47)[0][0])
x = Pk[k47:].astype(float) ** 2; w = ile[k47:].astype(float)
mm = np.ones(400001, bool); mm[:2] = False
for i in range(2, 633):
    if mm[i]: mm[i*i::i] = False
Q = np.nonzero(mm)[0]; Q = Q[Q >= 53]; etapy = np.concatenate(([47], Q))
C = [0.5, 0.55, 0.56, math.exp(-0.5772156649015329), 0.565, 0.57, 'z(x)']
# z(x): granica Polyi z modelu Banksa-Forda-Tao - najwieksza liczba pierwsza z prod_{p<=z}(1-1/p) >= 1/log x
Q_all = np.nonzero(mm)[0]; S_mert = np.cumsum(-np.log1p(-1.0 / Q_all.astype(float)))
ZX = Q_all[np.searchsorted(S_mert, np.log(np.log(x)), side='right') - 1]
idx = {c: np.clip(np.searchsorted(etapy, (ZX if c == 'z(x)' else x ** c), side='right') - 1, 0, len(etapy) - 1) for c in C}
wagi = {c: np.bincount(idx[c], weights=w, minlength=len(etapy)) for c in C}   # suma przerw z przedzialow na kazdym etapie
E = {c: np.zeros(len(wz)) for c in C}; Jv = np.arange(Jm, dtype=float); rows = np.arange(len(wz)); mi = mlen.astype(int)
ostatni = max(int(idx[c].max()) for c in C)
for t in range(ostatni + 1):
    if t > 0:
        q = float(etapy[t]); Rn = np.zeros_like(R); Rn[:, :-1] = R[:, 1:]
        R = ((q - Jv - 1) * R + (Jv + 1 - mlen[:, None]) * Rn) / (q - 1)
    for c in C:
        if wagi[c][t]: E[c] += wagi[c][t] * R[rows, mi]
kk = np.load('konst104_1e9.npz'); k2 = dict(map(tuple, kk['A2'])); k3 = dict(map(tuple, kk['A3']))
klucz = lambda s: (s[0]//2)*64 + s[1]//2 if len(s) == 2 else (s[0]//2)*4096 + (s[1]//2)*64 + s[2]//2
# obie orientacje osobno (jak w wersji 3): odbicie ma te sama prognoze
orient = []
for i, s in enumerate(wz):
    orient.append((s, i))
    if s != s[::-1]: orient.append((s[::-1], i))
def statystyki(c, zakres):
    out = []
    for m in (2, 3):
        sel = [(s, i) for s, i in orient if len(s) == m and zakres[0] <= sum(s) <= zakres[1] and E[c][i] > 0]
        Am = np.array([float((k2 if m == 2 else k3).get(klucz(s), 0)) for s, i in sel]); Em = np.array([E[c][i] for s, i in sel])
        Em = Em * Am.sum() / Em.sum()
        out.append((np.median(np.abs(Am - Em) / Em) * 100, ((Am - Em) ** 2 / Em).sum() / (len(sel) - 1), len(sel)))
    return out
for zakres in ((2, 40), (42, 104), (2, 104)):
    print('rozpietosc %d-%d:' % zakres)
    for c in C:
        (a1, b1, n1), (a2, b2, n2) = statystyki(c, zakres)
        print('   c = %s   pary: %6.2f%% %8.1f  (%d)   trojki: %6.2f%% %8.1f  (%d)' % (c if c == 'z(x)' else '%.4f' % c, a1, b1, n1, a2, b2, n2))

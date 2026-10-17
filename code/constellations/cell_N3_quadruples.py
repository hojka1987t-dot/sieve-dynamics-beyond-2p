# KOMORKA N3: czworki kolejnych luk (rozpietosc <= 104) na etapach 5# .. 47#.
# Etapy 5#..13#: pelne wyliczenie cyklu (numpy). Etapy 17#..43#: silnik konstelacji (kolo bazowe 13#).
# Na kazdym etapie: suma CRT dla kazdej konstelacji i kazdej luki, oraz zgodnosc sum po parach i trojkach
# z wierszami luk liczonymi niezaleznie (pelne wyliczenie albo silnik luk). Plik wynikowy osobno dla kazdego etapu;
# po przerwaniu uruchomic ponownie - gotowe etapy sa pomijane. Wymaga komorki A (konst_worker 4.5-K).
import os, sys, csv, time, multiprocessing, importlib
sys.path.insert(0, os.getcwd())
from math import prod, comb
import numpy as np
import konst_worker as KW
importlib.reload(KW)
assert KW.WERSJA == "4.5-K", "uruchom najpierw komorke A"

ROZP, R_BASE = 104, 6
PR = KW.generuj_pierwsze(15)

def _punkty(s):
    C = [0]
    for d in s: C.append(C[-1] + d)
    return C

def lista_konstelacji():
    dop = lambda s: all(len({c % p for c in _punkty(s)}) < p for p in PR)
    czw = [(a, b, c, d) for a in range(2, ROZP, 2) for b in range(2, ROZP - a, 2) for c in range(2, ROZP - a - b, 2)
           for d in range(2, ROZP + 1 - a - b - c, 2)]
    return sorted([s for s in czw if dop(s) and s <= s[::-1]], key=lambda s: (sum(s), s))

def _wprost(k, lista, luki):
    P = PR[:k]; N = prod(P)
    x = np.arange(N + ROZP + 1, dtype=np.int64); s = np.ones(x.size, bool)
    for p in P: s &= (x % p != 0)
    cs = np.concatenate(([0], np.cumsum(s, dtype=np.int64))); idx = np.arange(N)
    def rozklad(C):
        g = C[-1]; maska = np.ones(N, bool)
        for c in C: maska &= s[c:c + N]
        dod = (cs[idx + g] - cs[idx + 1])[maska] - (len(C) - 2)
        J, ile = np.unique(len(C) - 1 + dod, return_counts=True)
        return {int(a): int(b) for a, b in zip(J, ile)}
    return {t: rozklad(_punkty(t)) for t in lista}, {g: rozklad([0, g]) for g in luki}

def _silnik(k, lista, luki, watki):
    PB = prod(PR[:R_BASE]); K, G = {}, {}
    with multiprocessing.Pool(watki or multiprocessing.cpu_count()) as pool:
        for g, w in pool.imap_unordered(KW.zadanie, [(k, R_BASE, g, 1, PB + 1) for g in luki]): G[g] = w
        for t, w in pool.imap_unordered(KW.zadanie_konst, [(k, R_BASE, t, 1, PB + 1) for t in lista]): K[t] = w
    return K, G

def _kontrola(k, K, G):
    P = PR[:k]; bl = []
    for t, w in list(K.items()) + [((g,), w) for g, w in G.items()]:
        if sum(w.values()) != prod(p - len({c % p for c in _punkty(t)}) for p in P): bl.append(('CRT', t))
    pelne = {}
    for t, w in K.items(): pelne[t] = w; pelne[t[::-1]] = w
    for g in G:
        for m, wsp in ((4, lambda J: comb(J - 1, 3)),):
            suma = {}
            for t, w in pelne.items():
                if len(t) == m and sum(t) == g:
                    for J, c in w.items(): suma[J] = suma.get(J, 0) + c
            if suma != {J: wsp(J) * c for J, c in G[g].items() if wsp(J) > 0}: bl.append(('suma', g, m))
    return bl

def _zapisz(plik, wiersze):
    with open(plik + '.tmp', 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        for etyk, w in wiersze:
            jm = max(w) if w else 1
            wr.writerow([etyk, sum(w.values())] + [w.get(j, 0) for j in range(1, jm + 1)])
    os.replace(plik + '.tmp', plik)

def licz(etapy=range(3, 16), watki=None):
    lista = lista_konstelacji(); luki = list(range(2, ROZP + 1, 2))
    print('czworek na etap: %d' % len(lista), flush=True)
    for k in etapy:
        p = PR[k - 1]; plikK, plikG = 'nQ%d_czworki.csv' % p, 'nG%d_czw.csv' % p
        if os.path.exists(plikK) and os.path.exists(plikG):
            print('etap %d#: juz gotowy' % p, flush=True); continue
        t0 = time.time()
        K, G = (_wprost if k <= 6 else lambda k, l, g: _silnik(k, l, g, watki))(k, lista, luki)
        bl = _kontrola(k, K, G)
        if bl: raise RuntimeError('BLAD na etapie %d#: %s' % (p, bl[:5]))
        _zapisz(plikG, [('Gap Sum = %d' % g, G[g]) for g in luki])
        _zapisz(plikK, [('Constellation = ' + ','.join(map(str, t)), K[t]) for t in lista])
        print('etap %d#: gotowy w %.1f min; CRT i sumy po czworkach zgodne' % (p, (time.time() - t0) / 60), flush=True)
    print('GOTOWE', flush=True)

licz()

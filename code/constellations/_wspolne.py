"""Wspolne funkcje skryptow konstelacji: sciezki wzgledem repozytorium i odczyt plikow."""
import os, csv, gzip
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DATA = os.path.join(ROOT, 'data', 'constellations')
ETAPY = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
PR = [p for p in range(2, 60) if all(p % d for d in range(2, int(p ** .5) + 1))]

def czytaj(plik, klucz):
    """Wiersze 'klucz = a,b,...', suma, n_J dla J = 1, 2, ... -> {krotka: {J: n_J}}."""
    d = {}
    f = gzip.open(plik, 'rt', encoding='utf-8-sig') if plik.endswith('.gz') else open(plik, encoding='utf-8-sig')
    for r in csv.reader(f):
        if not r or not r[0].startswith(klucz): continue
        k = r[0].split('=')[1].strip()
        d[tuple(int(x) for x in k.split(','))] = {j + 1: int(c) for j, c in enumerate(r[2:]) if c.strip() and int(c)}
    return d

def konstelacje(m, p):
    plik = os.path.join(DATA, 'pairs_triples', 'nK%d_constellations.csv' % p) if m in (2, 3) else os.path.join(DATA, 'quadruples', 'nQ%d_quadruples.csv.gz' % p)
    return {s: w for s, w in czytaj(plik, 'Constellation').items() if len(s) == m}

def luki(p):
    plik = os.path.join(ROOT, 'data', 'nG47.csv') if p == 47 else os.path.join(DATA, 'gaps', 'nG%d_gaps.csv' % p)
    return czytaj(plik, 'Gap Sum')

def punkty(s):
    C = [0]
    for d in s: C.append(C[-1] + d)
    return C

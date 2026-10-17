# KOMORKA N (konstelacje): pary i trojki kolejnych luk o rozpietosci <= 104 przy 47# (k = 15).
# Wymaga komorki A. Kazda konstelacja sprawdzana od razu suma CRT; wynik zapisywany po kazdej; wznawianie.
# Liczona jest jedna konstelacja z kazdej pary odbic (s i s odwrocone maja rowne populacje).
import os, sys, csv, time, multiprocessing, importlib
sys.path.insert(0, os.getcwd())
from math import prod
import konst_worker as KW
importlib.reload(KW)
assert KW.WERSJA == "4.5-K", "uruchom najpierw komorke A"

K_ETAP, R_BASE, ROZP = 15, 6, 104          # 47#, kolo bazowe 13#, rozpietosc do 104
P = KW.generuj_pierwsze(K_ETAP); PB = prod(P[:R_BASE])

def _punkty(s):
    C = [0]
    for d in s: C.append(C[-1] + d)
    return C

def _dopuszczalna(s):
    C = _punkty(s)
    return all(len({c % p for c in C}) < p for p in P)

def lista_konstelacji():
    pary = [(a, b) for a in range(2, ROZP, 2) for b in range(2, ROZP + 1 - a, 2)]
    troj = [(a, b, c) for a in range(2, ROZP, 2) for b in range(2, ROZP - a, 2) for c in range(2, ROZP + 1 - a - b, 2)]
    wyb = [s for s in pary + troj if _dopuszczalna(s) and s <= s[::-1]]
    return sorted(wyb, key=lambda s: (len(s), sum(s), s))

def _gotowe(plik):
    d = set()
    if os.path.exists(plik):
        with open(plik, encoding='utf-8') as f:
            for r in csv.reader(f):
                if r and r[0].startswith('Constellation'):
                    d.add(tuple(int(x) for x in r[0].split('=')[1].split(',')))
    return d

def licz(plik='nK47_konstelacje.csv', watki=None):
    lista = lista_konstelacji(); gotowe = _gotowe(plik)
    zadania = [s for s in lista if s not in gotowe]
    print('konstelacji: %d, juz gotowych: %d, do policzenia: %d' % (len(lista), len(gotowe), len(zadania)), flush=True)
    t0 = time.time(); zrob = 0
    with multiprocessing.Pool(watki or multiprocessing.cpu_count()) as pool:
        # funkcja robocza MUSI byc w module (konst_worker), nie w notatniku: w Windows procesy potomne
        # nie widza funkcji zdefiniowanych w notatniku
        argumenty = [(K_ETAP, R_BASE, s, 1, PB + 1) for s in zadania]
        for s, w in pool.imap_unordered(KW.zadanie_konst, argumenty):
            crt = prod(p - len({c % p for c in _punkty(s)}) for p in P)
            if sum(w.values()) != crt:
                pool.terminate()
                raise RuntimeError('BLAD: suma dla %s = %d, a CRT = %d' % (s, sum(w.values()), crt))
            jmax = max(w)
            with open(plik, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(['Constellation = ' + ','.join(map(str, s)), sum(w.values())] + [w.get(j, 0) for j in range(1, jmax + 1)])
            zrob += 1
            if zrob % 200 == 0 or zrob == len(zadania):
                print('   %d/%d gotowe, %.1f min' % (zrob, len(zadania), (time.time() - t0) / 60), flush=True)
    print('GOTOWE; kazda konstelacja zgodna z suma CRT', flush=True)

licz()

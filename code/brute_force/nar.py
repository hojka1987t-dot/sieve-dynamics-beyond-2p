import numpy as np
from math import prod
from collections import defaultdict, Counter

def wskaznik(primes, okresy=3):
    N = prod(primes); a = np.ones(N, dtype=bool)
    for p in primes: a[::p] = False
    return N, np.tile(a, okresy)

def konstelacje(primes, mmax, Lmax):
    """Licznosci wszystkich konstelacji (ciagow m kolejnych luk), m<=mmax, rozpietosc<=Lmax."""
    N, a = wskaznik(primes, 2); cop = np.flatnonzero(a[:N])
    gaps = np.diff(np.append(cop, cop[0] + N)).tolist(); n = len(gaps)
    cnt = Counter()
    for i in range(n):
        s = 0; t = []
        for m in range(mmax):
            g = gaps[(i + m) % n]; s += g
            if s > Lmax: break
            t.append(g); cnt[tuple(t)] += 1
    return cnt

def B_s(primes, C, q):
    """Liczba czlonow napedzajacych s w G(N), ktorych punkty dodatkowe tworza
       JEDNA klase mod q, rozlaczna z klasami punktow C. Zwraca tez rozklad wg liczby punktow dodatkowych."""
    N, a = wskaznik(primes); L = C[-1]; Cs = set(C); Cr = {c % q for c in C}
    xs = np.flatnonzero(a[:N])
    for c in C[1:]: xs = xs[a[xs + c]]
    ile = 0; drogi = Counter()
    for x in xs.tolist():
        P = np.flatnonzero(a[x:x + L + 1]).tolist()
        E = [t for t in P if t not in Cs]
        if not E: continue
        r = {e % q for e in E}
        if len(r) == 1 and not (r & Cr):
            ile += 1; drogi[len(E)] += 1
    return ile, drogi

if __name__ == "__main__":
    print("PRAWO NARODZIN KONSTELACJI - sprawdzenie silowe")
    print()
    for P, q, mmax in [([2,3,5,7], 11, 4), ([2,3,5,7,11], 13, 4), ([2,3,5,11,13], 7, 3), ([2,3,5,7,11,13], 17, 3)]:
        Lmax = 4 * q
        przed = konstelacje(P, mmax, Lmax); po = konstelacje(P + [q], mmax, Lmax)
        narodz = [s for s in po if s not in przed]
        ok = 0; wiel = 0; zwykle = 0
        for s in narodz:
            C = [0]; 
            for g in s: C.append(C[-1] + g)
            b, drogi = B_s(P, C, q)
            ok += (b == po[s])
            if any(k > 1 for k in drogi): wiel += 1
            if 1 in drogi: zwykle += 1
        print("  %-20s -> %2d: rodzi sie %4d konstelacji; zgodnych z prawem %4d/%d; "
              "z droga zwykla %d, ze zlaniem wielopunktowym %d" % (str(P), q, len(narodz), ok, len(narodz), zwykle, wiel), flush=True)

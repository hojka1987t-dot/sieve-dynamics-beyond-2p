import numpy as np, random
from math import prod
from collections import defaultdict

def wskaznik(primes, okresy=3):
    N = prod(primes); a = np.ones(N, dtype=bool)
    for p in primes: a[::p] = False
    return N, np.tile(a, okresy)

def populacje(primes, C):
    """n_{s,J}: ile x mod N, dla ktorych wszystkie punkty C sa wzgl. pierwsze;
       J = liczba luk w oknie [x, x+|s|]. Zwraca tez punkty okien."""
    N, a = wskaznik(primes); L = C[-1]
    xs = np.flatnonzero(a[:N])
    for c in C[1:]: xs = xs[a[xs + c]]
    pop = defaultdict(int); okna = []
    for x in xs.tolist():
        P = np.flatnonzero(a[x:x + L + 1]).tolist()
        pop[len(P) - 1] += 1; okna.append(P)
    return dict(pop), okna

def przewidz(okna, C, q):
    Cs = set(C); pred = defaultdict(int); nielin = 0
    for P in okna:
        kl = defaultdict(list)
        for t in P: kl[t % q].append(t)
        J = len(P) - 1
        pred[J] += q - len(kl)
        for K in kl.values():
            if len(K) > 1: nielin += 1
            if Cs & set(K): continue          # zginal punkt samej konstelacji
            pred[J - len(K)] += 1
    return dict(pred), nielin

def test(primes, q, ile=40, seed=1):
    random.seed(seed)
    N, a = wskaznik(primes, 2); cop = np.flatnonzero(a[:N])
    gaps = np.diff(np.append(cop, cop[0] + N))
    kom = bl = nl = 0; zrobione = set()
    while len(zrobione) < ile:
        i = random.randrange(len(gaps)); m = random.randint(2, 6)
        s = tuple(gaps[(i + np.arange(m)) % len(gaps)].tolist())
        if not (2 * q <= sum(s) <= 5 * q) or s in zrobione: continue
        zrobione.add(s)
        C = [0] + np.cumsum(s).tolist()
        _, okna = populacje(primes, C)
        pred, n = przewidz(okna, C, q); nl += n
        fakt, _ = populacje(primes + [q], C)
        for J in set(pred) | set(fakt):
            kom += 1; bl += pred.get(J, 0) != fakt.get(J, 0)
    return kom, bl, nl

if __name__ == "__main__":
    print("Twierdzenie 1 dla KONSTELACJI (rozpietosci 2q..5q), sprawdzenie silowe")
    for P, q in [([2,3,5,7], 11), ([2,3,5,7,11], 13), ([2,3,5,7,11,13], 17), ([2,3,5,11,13], 7)]:
        k, b, n = test(P, q)
        print("  %-22s -> %2d : 40 konstelacji, komorek %4d, bledow %d, zlan wielopunktowych %d" % (str(P), q, k, b, n), flush=True)

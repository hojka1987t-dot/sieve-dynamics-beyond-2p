# Niezalezna weryfikacja silowa - bez zadnego kodu silnika zliczajacego.
from math import gcd, prod
from collections import defaultdict

def cykl(primes):
    N = prod(primes)
    return N, [x for x in range(1, N + 1) if gcd(x, N) == 1]

def czlony(N, cop, Gmax, z_punktami):
    """Wszystkie czlony (x, x+g) o g <= Gmax: kolejne liczby wzgl. pierwsze z N."""
    phi = len(cop)
    for i in range(phi):
        x = cop[i]; k = 1
        while True:
            y = cop[(i + k) % phi] + N * ((i + k) // phi)
            g = y - x
            if g > Gmax: break
            if z_punktami:
                pts = [cop[(i + m) % phi] + N * ((i + m) // phi) - x for m in range(k + 1)]
                yield g, k, pts
            else:
                yield g, k, None
            k += 1

def test(primes, q, Gmax):
    N, cop = cykl(primes)
    Nq, copq = cykl(primes + [q])
    pred = defaultdict(int); fakt = defaultdict(int)
    maxkl = 1; zab = 0; rat = 0
    for g, j, pts in czlony(N, cop, Gmax, True):
        kl = defaultdict(list)
        for t in pts: kl[t % q].append(t)
        pred[(g, j)] += q - len(kl)
        for c in kl.values():
            maxkl = max(maxkl, len(c))
            if 0 in c or g in c:
                if j == 2 and len(c) == 2: zab += 1        # czlon 2-lukowy: punkt w klasie konca
                continue
            pred[(g, j - len(c))] += 1
            if j == 3 and len(c) == 2: rat += 1              # czlon 3-lukowy: dwa punkty wewn. razem
    for g, j, _ in czlony(Nq, copq, Gmax, False):
        fakt[(g, j)] += 1
    kl_ = set(pred) | set(fakt)
    bl = [k for k in kl_ if pred.get(k, 0) != fakt.get(k, 0)]
    return len(kl_), len(bl), maxkl, zab, rat, max(g for g, j in fakt)

TESTY = [("7#  -> 11", [2,3,5,7], 11, 80),
         ("11# -> 13", [2,3,5,7,11], 13, 90),
         ("13# -> 17", [2,3,5,7,11,13], 17, 110),
         ("sito bez 7:  {2,3,5,11,13} -> 7", [2,3,5,11,13], 7, 70),
         ("sito bez 5:  {2,3,7,11,13} -> 5", [2,3,7,11,13], 5, 60),
         ("sito bez 11: {2,3,5,7,13,17} -> 11", [2,3,5,7,13,17], 11, 90)]
if __name__ == "__main__":
    print("TWIERDZENIE W WERSJI OGOLNEJ (dowolne klasy reszt), sprawdzenie silowe calych cykli")
    print()
    print("  przejscie                             komorek  bledow  max klasa  zabojstw  ratunkow  (g do)")
    for nm, P, q, G in TESTY:
        n, b, mk, z, r, gm = test(P, q, G)
        print("  %-36s %6d   %4d      %d       %6d   %6d     %d" % (nm, n, b, mk, z, r, gm))

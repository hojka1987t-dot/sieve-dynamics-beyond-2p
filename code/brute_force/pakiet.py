import numpy as np, random
from itertools import combinations
from math import comb
from collections import defaultdict
from kon import wskaznik, populacje

def test(primes, q, ile=60, seed=3):
    random.seed(seed)
    N, a = wskaznik(primes, 2); cop = np.flatnonzero(a[:N])
    gaps = np.diff(np.append(cop, cop[0] + N))
    st = {'lump_ponizej': [0, 0], 'lump_powyzej_bez': [0, 0], 'lump_powyzej_z': [0, 0], 'mom': [0, 0]}
    zrob = set()
    while len(zrob) < ile:
        i = random.randrange(len(gaps)); m = random.randint(2, 4)
        s = tuple(gaps[(i + np.arange(m)) % len(gaps)].tolist())
        if not (q <= sum(s) <= 4 * q) or s in zrob: continue
        C = [0] + np.cumsum(s).tolist(); Cs = set(C)
        _, okna = populacje(primes, C)
        if any(len(P) - len(C) > 11 for P in okna): continue
        zrob.add(s)
        nN = defaultdict(int)
        for P in okna: nN[len(P) - 1] += 1
        nQ, _ = populacje(primes + [q], C)
        # (1) zlepienie Holta: n'_J = (q-J-1) n_J + (J+1-m) n_{J+1}
        Jmax = max(nN) + 1
        lump = {J: (q - J - 1) * nN.get(J, 0) + (J + 1 - m) * nN.get(J + 1, 0) for J in range(m, Jmax + 1)}
        dokladne = all(lump.get(J, 0) == nQ.get(J, 0) for J in set(lump) | set(nQ))
        wielo = any(len({t % q for t in P}) < len(P) for P in okna)
        klucz = 'lump_ponizej' if sum(s) < 2 * q else ('lump_powyzej_z' if wielo else 'lump_powyzej_bez')
        st[klucz][0] += 1; st[klucz][1] += dokladne
        # (2) momenty: S_k(qN) = (q-m-1-k) S_k(N) + Pi_k
        for k in range(0, 4):
            SkN = sum(comb(J - m, k) * v for J, v in nN.items())
            SkQ = sum(comb(J - m, k) * v for J, v in nQ.items())
            Pi = 0
            for P in okna:
                E = [t for t in P if t not in Cs]
                for T in combinations(E, k):
                    A = C + list(T)
                    Pi += len(A) - len({t % q for t in A})
            st['mom'][0] += 1; st['mom'][1] += (SkQ == (q - m - 1 - k) * SkN + Pi)
    return st

if __name__ == "__main__":
    for P, q in [([2,3,5,7], 11), ([2,3,5,7,11], 13), ([2,3,5,11,13], 7)]:
        st = test(P, q)
        print("%-18s -> %2d" % (str(P), q))
        print("   rekurencja Holta, rozpietosc < 2q:                      dokladna w %d z %d" % (st['lump_ponizej'][1], st['lump_ponizej'][0]))
        print("   rekurencja Holta, >= 2q, bez punktow przystajacych:      dokladna w %d z %d" % (st['lump_powyzej_bez'][1], st['lump_powyzej_bez'][0]))
        print("   rekurencja Holta, >= 2q, z punktami przystajacymi:       dokladna w %d z %d" % (st['lump_powyzej_z'][1], st['lump_powyzej_z'][0]))
        print("   postac w momentach (k = 0..3):                          zgodna w %d z %d" % (st['mom'][1], st['mom'][0]), flush=True)

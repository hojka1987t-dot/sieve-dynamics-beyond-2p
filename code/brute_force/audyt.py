import numpy as np, random
from math import prod, gcd
from collections import defaultdict, Counter
from itertools import combinations

def wsk(P, okresy=4):
    N = prod(P); a = np.ones(N, dtype=bool)
    for p in P: a[::p] = False
    return N, np.tile(a, okresy)

def okna(P, C):
    """Wszystkie x mod N z punktami C wzgl. pierwszymi; zwraca zbiory punktow okien."""
    N = prod(P); L = C[-1]
    N, a = wsk(P, L // N + 3)
    xs = np.flatnonzero(a[:N])
    for c in C[1:]: xs = xs[a[xs + c]]
    return [np.flatnonzero(a[x:x + L + 1]).tolist() for x in xs.tolist()]

def pop(P, C):
    c = Counter(len(W) - 1 for W in okna(P, C)); return dict(c)

def tw4(P, C, q):
    """Twierdzenie 4 (dla m=1 to Twierdzenie 1): przewidywane n_{s,J}(qN)."""
    Cs = set(C); pr = defaultdict(int)
    for W in okna(P, C):
        kl = defaultdict(list)
        for t in W: kl[t % q].append(t)
        pr[len(W) - 1] += q - len(kl)
        for K in kl.values():
            if not (Cs & set(K)): pr[len(W) - 1 - len(K)] += 1
    return dict(pr)

def zgodne(a, b): return all(a.get(k, 0) == b.get(k, 0) for k in set(a) | set(b))

if __name__ == "__main__":
    wyn = {}
    import sys
    class D_(dict):
        def __setitem__(self,k,v):
            super().__setitem__(k,v); print('  %-78s %s' % (k, '%s/%s' % v), flush=True)
    wyn = D_()
    # A. Tw. 1/4 dla luk: g az do N-2, a takze g >= N; w tym wykluczony przypadek N = 2
    for P, q, G in [([2], 3, 12), ([2], 5, 12), ([2,3], 5, 18), ([2,3,5], 7, 58), ([2,3,5,7], 11, 208), ([2,3,5,11], 7, 120)]:
        N = prod(P); ok = tot = 0; pow_N = 0
        for g in range(2, G + 1, 2):
            p1 = tw4(P, [0, g], q); p2 = pop(P + [q], [0, g])
            tot += 1; ok += zgodne(p1, p2); pow_N += (g >= N)
        wyn['A %s->%d (g do %d, w tym %d rozp. >= N)' % (P, q, G, pow_N)] = (ok, tot)
    # B. Tw. 3 (narodziny) = wiersz J=1 z A - sprawdzany razem; tu osobno zbior D(qN)
    for P, q in [([2], 3), ([2,3], 5), ([2,3,5], 7), ([2,3,5,7], 11), ([2,3,5,7,11], 13)]:
        N, a = wsk(P); cop = np.flatnonzero(a[:N]); gaps = np.diff(np.append(cop, cop[0] + N))
        D = set(gaps.tolist()); m = gaps % (2*q) == 0; Pn = np.flatnonzero(~m)
        cs = np.concatenate(([0], np.cumsum(np.concatenate((gaps, gaps)))))
        nx = np.roll(Pn, -1); nx = np.where(nx > Pn, nx, nx + len(gaps))
        ur = set((cs[nx + 1] - cs[Pn]).tolist())
        N2, a2 = wsk(P + [q]); c2 = np.flatnonzero(a2[:N2]); D2 = set(np.diff(np.append(c2, c2[0] + N2)).tolist())
        wyn['B prawo narodzin (zbiory) %s->%d, H(qN)=%d, N=%d' % (P, q, max(D2), N)] = (int(D | ur == D2), 1)
    # D. Tw. 4 dla konstelacji o rozpietosci blisko N i powyzej N
    random.seed(4)
    for P, q in [([2,3,5], 7), ([2,3,5,7], 11)]:
        N, a = wsk(P); cop = np.flatnonzero(a[:N]).tolist(); ok = tot = 0; bl = 0
        while tot < 30:
            i = random.randrange(len(cop)); cel = random.randint(N - 12, N + 40)
            pts = [cop[i]]; k = i
            while pts[-1] - pts[0] < cel:
                k += 1; pts.append(cop[k % len(cop)] + N * (k // len(cop)))
            C = [t - pts[0] for t in pts]
            tot += 1; ok += zgodne(tw4(P, C, q), pop(P + [q], C))
        wyn['D konstelacje %s->%d, rozpietosc od N-12 do N+40' % (P, q)] = (ok, tot)
    # E. Lemat 6 i Wniosek 5.1 w lancuchu 2 -> 6 -> 30 -> 210 -> 2310 -> 30030
    lanc = [[2], [2,3], [2,3,5], [2,3,5,7], [2,3,5,7,11], [2,3,5,7,11,13]]
    konst = set()
    for m_ in (1, 2, 3):
        for s in __import__('itertools').product([2,4,6,8,10,12,14], repeat=m_):
            if sum(s) <= 36: konst.add(s)
    trw = znik_na_zawsze = pierwsze_ok = pierwsze_tot = 0; zle = []
    for s in sorted(konst):
        C = [0]
        for g in s: C.append(C[-1] + g)
        obecna = [pop(P, C).get(len(s), 0) > 0 for P in lanc]
        # trwalosc / znikanie
        for i in range(len(lanc) - 1):
            q = lanc[i + 1][-1]; nu = len({c % q for c in C})
            if obecna[i] and nu < q and not obecna[i + 1]: zle.append(('zniknela mimo dopuszczalnosci', s, i))
            if obecna[i] and nu == q and obecna[i + 1]: zle.append(('przetrwala mimo niedopuszczalnosci', s, i))
        for i in range(len(lanc) - 1):
            if obecna[i] and not obecna[i + 1] and any(obecna[i + 2:]): zle.append(('wrocila po zniknieciu', s, i))
        # pierwsze pojawienie sie: Wn. 5.1
        for i in range(len(lanc) - 1):
            q = lanc[i + 1][-1]
            Cr = {c % q for c in C}; Cs = set(C)
            B = 0
            for W in okna(lanc[i], C):
                E = [t for t in W if t not in Cs]
                if E and len({e % q for e in E}) == 1 and not ({e % q for e in E} & Cr): B += 1
            przew = (not obecna[i]) and B > 0
            fakt = obecna[i + 1] and not any(obecna[:i + 1])
            pierwsze_tot += 1; pierwsze_ok += (przew == fakt)
    wyn['E Lemat 6: trwalosc/znikanie/powroty (%d konstelacji)' % len(konst)] = (len(konst) - len({z[1] for z in zle}), len(konst))
    wyn['E Wniosek 5.1: pierwsze pojawienie sie w lancuchu (przypadki)'] = (pierwsze_ok, pierwsze_tot)
    # F. Tw. 6: warunek wystarczajacy - oraz szukanie kontrprzykladu na koniecznosc
    random.seed(6); suf_ok = suf_tot = 0; kontr = []
    for P, q in [([2,3,5,7], 11), ([2,3,5,7,11], 13), ([2,3,5,11,13], 7), ([2,3,7,11,13], 5)]:
        N, a = wsk(P); cop = np.flatnonzero(a[:N]).tolist(); proby = 0
        while proby < 150:
            i = random.randrange(len(cop)); j = i + random.randint(2, 5)
            pts = [cop[k % len(cop)] + N * (k // len(cop)) for k in range(i, j + 1)]
            C = [t - pts[0] for t in pts]; m_ = len(C) - 1
            if C[-1] > 5 * q: continue
            proby += 1
            W = okna(P, C); nN = Counter(len(w) - 1 for w in W)
            fakt = pop(P + [q], C); Jm = max(nN) + 1
            lump = {J: (q - J - 1) * nN.get(J, 0) + (J + 1 - m_) * nN.get(J + 1, 0) for J in range(m_, Jm + 1)}
            dokl = zgodne(lump, fakt)
            wielo = any(len({t % q for t in w}) < len(w) for w in W)
            if not wielo: suf_tot += 1; suf_ok += dokl
            elif dokl: kontr.append((P, q, tuple(C)))
    wyn['F Tw. 6 jako warunek wystarczajacy'] = (suf_ok, suf_tot)
    wyn['F kontrprzyklady na koniecznosc (punkty przystajace, a lancuch Holta dokladny)'] = (len(kontr), '-')
    pass
    if zle: print('  NIEZGODNOSCI:', zle[:5])
    if kontr: print('  przyklad kontrprzykladu:', kontr[0])

import numpy as np
from math import prod

def cykl(primes):
    N = prod(primes)
    a = np.ones(N, dtype=bool)
    for p in primes: a[::p] = False
    cop = np.flatnonzero(a).astype(np.int64)
    gaps = np.diff(np.append(cop, cop[0] + N))
    return gaps

def narodziny(gaps, q):
    """Sumy kwalifikujacych sie konstelacji (Tw. 3): luka nie-wielokrotnosc 2q,
    dowolnie wiele luk-wielokrotnosci 2q, luka nie-wielokrotnosc 2q."""
    m = (gaps % (2 * q) == 0)
    P = np.flatnonzero(~m)
    cs = np.concatenate(([0], np.cumsum(np.concatenate((gaps, gaps)))))
    nxt = np.roll(P, -1); nxt = np.where(nxt > P, nxt, nxt + len(gaps))
    sumy = cs[nxt + 1] - cs[P]
    return set(np.unique(sumy).tolist())

def pary_wszystkie(gaps):
    return set(np.unique(gaps + np.roll(gaps, -1)).tolist())

def pary_kwal(gaps, q):
    m = (gaps % (2 * q) == 0); mn = np.roll(m, -1)
    s = (gaps + np.roll(gaps, -1))[~m & ~mn]
    return set(np.unique(s).tolist())

def badaj(nazwa, S):
    wyn = {'nazwa': nazwa, 'prawo_ok': True, 'trwale': [], 'zabojstwa': [], 'cienie': [], 'brak': []}
    G = [cykl(S[:t]) for t in range(1, len(S) + 1)]
    D = [set(np.unique(g).tolist()) for g in G]
    h = [max(d) for d in D]
    for t in range(1, len(S)):
        q = S[t]
        przew = D[t - 1] | narodziny(G[t - 1], q)
        if przew != D[t]:
            wyn['prawo_ok'] = False
        M2 = max(pary_kwal(G[t - 1], q) | {0})
        wsz = pary_wszystkie(G[t - 1])
        for g in range(2, h[t], 2):
            if g in D[t]: continue
            wyn['brak'].append((t + 1, g))
            if g <= h[t - 1]:
                wyn['trwale'].append((t + 1, g))
            if g in wsz:
                wyn['zabojstwa'].append((t + 1, g))
            if g > M2:
                wyn['cienie'].append((t + 1, g))
    return wyn

SITA = [
 ("kontrola: kolejne l. pierwsze",  [2,3,5,7,11,13,17,19]),
 ("bez 3",                          [2,5,7,11,13,17,19]),
 ("bez 5",                          [2,3,7,11,13,17,19,23]),
 ("bez 7",                          [2,3,5,11,13,17,19,23]),
 ("bez 11",                         [2,3,5,7,13,17,19,23]),
 ("bez 13",                         [2,3,5,7,11,17,19,23]),
 ("zamiana 11 i 13",                [2,3,5,7,13,11,17,19]),
 ("19 wczesnie",                    [2,3,5,19,7,11,13,17]),
 ("bez 3 i 5",                      [2,7,11,13,17,19,23]),
 ("bez 5 i 7",                      [2,3,11,13,17,19,23]),
]
if __name__ == "__main__":
    print("  sito                            prawo narodzin  brakujacych  TRWALE dziury   zabojstwa   cienie")
    for nm, S in SITA:
        w = badaj(nm, S)
        print("  %-32s %-14s  %6d       %-14s %-11s %s" % (nm, 'zgodne' if w['prawo_ok'] else 'NIEZGODNE',
              len(w['brak']), str(len(w['trwale'])) + ((' ' + str(w['trwale'][:3])) if w['trwale'] else ''),
              len(w['zabojstwa']), len(w['cienie'])), flush=True)

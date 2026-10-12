"""Wyczerpujaca weryfikacja Czesci I (sieve beyond 2p) na pelnych cyklach.
(1) Tozsamosc ksztaltow (Tw. 3.4 i 5.1 dla WSZYSTKICH konstelacji o rozpietosci <= S):
    m_P(qN) = (q - nu_q(P)) m_P(N) + sum_K m_{P u K}(N),  K = pelna klasa mod q bez koncow.
(2) Dla kazdej konstelacji s o rozpietosci <= S_s: prawo narodzin (Tw. 4.1), lancuch Holta na dlugosciach,
    warunek Tw. 5.1 (brak zaludnionego ksztaltu z dwoma punktami przystajacymi mod q) i kryterium Q(s) Holta.
Uzycie: python weryfikacja_wyczerpujaca.py "2,3,5,7" 11 40 24"""
import sys, time
import numpy as np
from collections import defaultdict

def ksztalty(primes, S):
    N = int(np.prod(primes))
    a = np.arange(N + S + 2, dtype=np.int64); ok = np.ones(a.size, bool)
    for p in primes: ok &= (a % p != 0)
    pos = a[ok]; phi = int(np.count_nonzero(pos < N))
    pos = np.concatenate((pos, np.full(S // 2 + 5, 10**12, dtype=np.int64)))   # wartownik
    idx = np.arange(phi); m = np.ones(phi, dtype=np.int64); rec = []
    J = 1
    while True:
        off = pos[idx + J] - pos[idx]; v = off <= S
        if not v.any(): break
        m = m | (np.int64(1) << (off // 2)); rec.append(m[v].copy()); J += 1
    u, c = np.unique(np.concatenate(rec), return_counts=True)
    return N, dict(zip(u.tolist(), c.tolist()))

def punkty(mask):
    out = []; b = 0
    while mask:
        if mask & 1: out.append(2 * b)
        mask >>= 1; b += 1
    return out

def klasy(pts, q):
    d = defaultdict(list)
    for t in pts: d[t % q].append(t)
    return list(d.values())

def maska(pts): return sum(1 << (t // 2) for t in pts)

def q_max(C):
    Q = set()
    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            n = C[j] - C[i]; p = 2
            while p * p <= n:
                if n % p == 0:
                    Q.add(p)
                    while n % p == 0: n //= p
                p += 1
            if n > 1: Q.add(n)
    return max(Q)

def uruchom(primes, q, S, Ss):
    t0 = time.time()
    N, mN = ksztalty(primes, S); _, mQ = ksztalty(primes + [q], S)
    # (1) tozsamosc ksztaltow
    pred = defaultdict(int)
    for P0, c in mN.items():
        pts = punkty(P0); L = pts[-1]; K = klasy(pts, q)
        pred[P0] += (q - len(K)) * c
        for k in K:
            if 0 in k or L in k: continue
            pred[P0 & ~maska(k)] += c
    klucze = set(pred) | set(mQ)
    bledy1 = sum(1 for P in klucze if pred.get(P, 0) != mQ.get(P, 0))
    # (2) konstelacje o rozpietosci <= Ss
    nN = defaultdict(lambda: defaultdict(int)); nQ = defaultdict(lambda: defaultdict(int))
    kong = defaultdict(bool); B = defaultdict(int)
    def rozloz(mapa, cel, zrodlo):
        for P, c in mapa.items():
            pts = punkty(P); L = pts[-1]
            if L > Ss: continue
            wew = pts[1:-1]; J = len(pts) - 1
            dwa = zrodlo and any(len(k) > 1 for k in klasy(pts, q))
            for r in range(1 << len(wew)):
                Cpts = [0] + [wew[i] for i in range(len(wew)) if r >> i & 1] + [L]
                key = tuple(Cpts); cel[key][J] += c
                if zrodlo:
                    if dwa: kong[key] = True
                    E = [t for t in pts if t not in set(Cpts)]
                    if E and len({t % q for t in E}) == 1 and (E[0] % q) not in {t % q for t in Cpts}:
                        B[key] += c
    rozloz(mN, nN, True); rozloz(mQ, nQ, False)
    st = defaultdict(int); bledy_ur = 0; holt_zle = 0; holt_dobre = 0
    for C, d in nN.items():
        m = len(C) - 1; nu = len({t % q for t in C})
        if nQ[C][m] != (q - nu) * d.get(m, 0) + B[C]: bledy_ur += 1
        Js = set(d) | set(nQ[C])
        lancuch = all(nQ[C].get(J, 0) == (q - J - 1) * d.get(J, 0) + (J + 1 - m) * d.get(J + 1, 0) for J in Js)
        a = not kong[C]
        st[(a, lancuch)] += 1
        holt = q > q_max(list(C))
        if holt and not a: holt_zle += 1
        if holt and a: holt_dobre += 1
    nazwa = "*".join(map(str, primes))
    print(f"N={nazwa} -> q={q}: ksztaltow (rozp. <= {S}) w N: {len(mN)}, w qN: {len(mQ)}; tozsamosc ksztaltow: {len(klucze) - bledy1}/{len(klucze)} zgodnych")
    print(f"   konstelacji (rozp. <= {Ss}): {len(nN)}; prawo narodzin: {len(nN) - bledy_ur}/{len(nN)} zgodnych")
    print(f"   warunek Tw.5.1 / lancuch Holta dokladny: tak/tak {st[(True,True)]}, tak/nie {st[(True,False)]} (powinno byc 0), "
          f"nie/tak {st[(False,True)]} (kontrprzyklady do koniecznosci), nie/nie {st[(False,False)]}")
    print(f"   kryterium Holta q > q_max(Q(s)): przewiduje jednolitosc {holt_dobre + holt_zle} razy, w tym bledne {holt_zle}   ({time.time() - t0:.0f} s)")

if __name__ == "__main__":
    pr = [int(x) for x in sys.argv[1].split(",")]
    uruchom(pr, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

# KOMORKA A (wersja 4.5) - zapisuje workera holt_worker.py (bez %%writefile). Uruchom, potem komorke C.
# Wynik identyczny z 4.1 (sprawdzone okno po oknie i na calych lukach); zmiany:
#   1. wlaczenia-wylaczenia zamiast DP po maskach (jak 4.3): f(T) = prod_p (b_p - nu_p(T)), potem dokladne odwrocenie;
#   2. symetria x -> -x (liczone jedno okno z pary odbic);
#   3. podzbiory w blokach 2^BLOK: pamiec na proces ok. (liczba fal + 8) * 8 * 2^BLOK bajtow (BLOK = 21: ok. 0,4 GB),
#      niezaleznie od liczby wezlow okna;
#   4. reszty wezlow mod p numerowane w obrebie okna (dowolnie duze p);
#   5. gdy iloczyn liczb klas przekracza 2^63: fale w grupach z iloczynem < 2^63, sumy modulo kilku liczb pierwszych
#      < 2^31 i chinskie twierdzenie o resztach (dokladnie, bez ograniczenia etapu).
# Wymaga numpy (najlepiej >= 2.0); uruchamiac w CPythonie.
kod = r'''
from math import gcd, comb
import numpy as np
WERSJA = "4.5"
MODULY = [2147483647, 2147483629, 2147483587, 2147483579, 2147483563, 2147483549, 2147483543, 2147483497]   # liczby pierwsze < 2^31
BLOK = 21          # podzbiory przetwarzane w blokach po 2^BLOK: pamiec na okno ok. (liczba fal + 6) * 8 * 2^BLOK bajtow

try:
    _bitcount = np.bitwise_count
except AttributeError:                       # numpy < 2.0
    _LUT = np.array([bin(i).count("1") for i in range(1 << 16)], dtype=np.uint8)
    def _bitcount(x):
        x = x.astype(np.uint64)
        return (_LUT[x & 0xFFFF].astype(np.int64) + _LUT[(x >> 16) & 0xFFFF] + _LUT[(x >> 32) & 0xFFFF] + _LUT[x >> 48])

def generuj_pierwsze(n):
    pr = []; x = 2
    while len(pr) < n:
        if all(x % p for p in pr if p * p <= x): pr.append(x)
        x += 1
    return pr

_PC = {}
def _popcount_T(n):
    a = _PC.get(n)
    if a is None:
        a = np.asarray(_bitcount(np.arange(1 << n, dtype=np.uint64))).astype(np.intp)
        _PC[n] = a
    return a

def rozklad_csp(wezly, fale, g, blok=None, wymus_mod=False):
    """Wynik jak w 4.1/4.3/4.4.  Wlaczenia-wylaczenia: f(T) = prod_p (b_p - nu_p(T)), S_k = sum_{|T|=k} f(T),
    v[m] = sum_{k>=m} (-1)^(k-m) C(k,m) S_k.  Jak 4.4 (reszty numerowane w obrebie okna, bloki 2^BLOK), a gdy iloczyn
    liczb klas przekracza 2^63: fale dzielone na grupy z iloczynem < 2^63 (dokladnie w int64), S_k liczone modulo kilku
    liczb pierwszych < 2^31 i skladane chinskim twierdzeniem o resztach (dokladnie, bo 0 <= S_k < iloczyn modulow)."""
    blok = BLOK if blok is None else blok
    N = len(wezly)
    prim = []
    for p in fale:
        em = g % p
        b = (p - 1) if em == 0 else (p - 2)
        idx = {}; kody = []
        for w in wezly:
            r = w % p
            kody.append(idx.setdefault(r, len(idx)) if (r != 0 and r != em) else -1)
        assert len(idx) <= 64
        prim.append((b, kody))
    grupy = []; cur = []; pc_ = 1; bprod = 1
    for i, (b, _) in enumerate(prim):
        bprod *= b
        if cur and (pc_ * b >= 2 ** 63 or wymus_mod):
            grupy.append(cur); cur = []; pc_ = 1
        cur.append(i); pc_ *= b
    grupy.append(cur)
    modularnie = len(grupy) > 1
    if modularnie:
        granica = (1 << N) * bprod            # 0 <= S_k <= C(N,k) * bprod < 2^N * bprod
        r = 1; Mprod = MODULY[0]
        while Mprod <= granica:
            assert r < len(MODULY), "za malo modulow"
            Mprod *= MODULY[r]; r += 1
        mods = MODULY[:r]
        Smod = [[0] * (N + 1) for _ in mods]
    nL = min(N, blok); nH = N - nL; ML = 1 << nL
    RL = []
    for b, kody in prim:
        R = np.zeros(ML, dtype=np.uint64)
        for i in range(nL):
            h = 1 << i
            if kody[i] >= 0:
                np.bitwise_or(R[:h], np.uint64(1 << kody[i]), out=R[h:2 * h])
            else:
                R[h:2 * h] = R[:h]
        RL.append(R)
    pcL = _popcount_T(nL)
    S = [0] * (N + 1)
    fg = [np.empty(ML, dtype=np.int64) for _ in grupy]
    for hm in range(1 << nH):
        dh = bin(hm).count("1")
        zero = False
        for f, grupa in zip(fg, grupy):
            f.fill(1)
            for i in grupa:
                b, kody = prim[i]; R = RL[i]
                rh = 0
                for t in range(nH):
                    if hm >> t & 1 and kody[nL + t] >= 0:
                        rh |= 1 << kody[nL + t]
                if bin(rh).count("1") >= b:      # klasy wyczerpane: f = 0 dla calego bloku
                    zero = True; break
                if rh:
                    f *= b - np.asarray(_bitcount(R | np.uint64(rh))).astype(np.int64)
                else:
                    f *= b - np.asarray(_bitcount(R)).astype(np.int64)
            if zero:
                break
        if zero:
            continue
        if not modularnie:
            f = fg[0]
            for sh in (0, 21, 42):               # czesci < 2^21, sumy < 2^(21+BLOK) < 2^53: dokladne w float64
                s = np.bincount(pcL, weights=((f >> sh) & ((1 << 21) - 1)).astype(np.float64), minlength=nL + 1)
                for k in range(nL + 1):
                    S[k + dh] += int(s[k]) << sh
        else:
            for j, m in enumerate(mods):
                F = fg[0] % m
                for G in fg[1:]:
                    F = (F * (G % m)) % m        # < 2^62
                s = np.bincount(pcL, weights=F.astype(np.float64), minlength=nL + 1)   # sumy < 2^(31+BLOK) <= 2^53
                for k in range(nL + 1):
                    Smod[j][k + dh] = (Smod[j][k + dh] + int(s[k])) % m
    if modularnie:
        for k in range(N + 1):                   # chinskie twierdzenie o resztach
            x = 0; M = 1
            for j, m in enumerate(mods):
                t = ((Smod[j][k] - x) * pow(M, -1, m)) % m
                x += M * t; M *= m
            S[k] = x
    return [sum((-1) ** (k - m) * comb(k, m) * S[k] for k in range(m, N + 1)) for m in range(N + 1)]

def zadanie(args):
    """(k, r_base, g, v0_od, v0_do) -> (g, {j: n_{g,j} z tego zakresu okien}); symetria x -> -x jak w 4.3."""
    k, r_base, g, a, b = args
    pr = generuj_pierwsze(k); Pb = 1
    for p in pr[:r_base]: Pb *= p
    fale = pr[r_base:k]
    wynik = {}
    for v0 in range(a, b):
        if gcd(v0, Pb) != 1 or gcd(v0 + g, Pb) != 1: continue
        v1 = (-v0 - g) % Pb
        if v1 < v0: continue
        waga = 1 if v1 == v0 else 2
        wez = [i for i in range(1, g) if gcd(v0 + i, Pb) == 1]
        for m, c in enumerate(rozklad_csp(wez, fale, g)):
            if c: wynik[m + 1] = wynik.get(m + 1, 0) + waga * c
    return g, wynik
'''
with open('holt_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('holt_worker.py'), 'bajtow do', os.getcwd(), '(wersja 4.5)')

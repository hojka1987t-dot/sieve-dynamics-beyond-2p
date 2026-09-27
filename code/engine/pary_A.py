# KOMORKA A - zapis workera (bez %%writefile). Uruchom, potem komorke B.
kod = r'''
from math import gcd
from collections import defaultdict
WERSJA = "5.0"

def generuj_pierwsze(n):
    pr = []; x = 2
    while len(pr) < n:
        if all(x % p for p in pr if p * p <= x): pr.append(x)
        x += 1
    return pr

def rozklad_pary(wezly, fale, g, q):
    """Dla jednego okna: liczba przypisan fal endgame wg struktury powstalego czlonu:
       klucz (j, IE, II) wzgledem nastepnej liczby pierwszej q, gdzie
       j  = dlugosc czlonu (1 + liczba niepokrytych wezlow),
       IE = ile punktow wewnetrznych lezy dokladnie 2q od konca (0, 1 lub 2),
       II = ile par punktow wewnetrznych jest odleglych dokladnie o 2q.
       Tylko takie pary zlewaja sie przy q naraz (punkty sa nieparzyste). Wymaga g < 4q."""
    assert g < 4 * q
    N = len(wezly); K = len(fale)
    idx = {w: i for i, w in enumerate(wezly)}
    mL = (1 << idx[2 * q]) if (2 * q) in idx else 0
    mR = (1 << idx[g - 2 * q]) if (g - 2 * q) in idx else 0
    pary = [(1 << idx[t]) | (1 << idx[t + 2 * q]) for t in wezly if (t + 2 * q) in idx]
    warstwy = []
    for p in fale:
        em = g % p; d = {}
        for i, w in enumerate(wezly):
            r = w % p
            if r != 0 and r != em:
                d[r] = d.get(r, 0) | (1 << i)
        b = (p - 1) if em == 0 else (p - 2)
        grup = {}
        for r, m in d.items():
            grup[m] = grup.get(m, 0) + 1
        puste = b - len(d)
        if puste > 0:
            grup[0] = grup.get(0, 0) + puste
        warstwy.append(list(grup.items()))
    memo = {}
    def f(i, unc):
        if i == K:
            ie = (1 if unc & mL else 0) + (1 if unc & mR else 0)
            ii = sum(1 for pm in pary if unc & pm == pm)
            return {(bin(unc).count('1') + 1, ie, ii): 1}
        k = (i, unc); r = memo.get(k)
        if r is not None: return r
        acc = defaultdict(int)
        for m, kr in warstwy[i]:
            for key, c in f(i + 1, unc & ~m).items():
                acc[key] += kr * c
        memo[k] = dict(acc); return memo[k]
    return f(0, (1 << N) - 1)

def zadanie(args):
    """(k, r_base, g, q, v0_od, v0_do) -> (g, {(j,IE,II): liczba czlonow w G(p_k#)})"""
    k, r_base, g, q, a, b = args
    pr = generuj_pierwsze(k); Pb = 1
    for p in pr[:r_base]: Pb *= p
    fale = pr[r_base:k]
    wyn = defaultdict(int)
    for v0 in range(a, b):
        if gcd(v0, Pb) != 1 or gcd(v0 + g, Pb) != 1: continue
        wez = [i for i in range(1, g) if gcd(v0 + i, Pb) == 1]
        for key, c in rozklad_pary(wez, fale, g, q).items():
            wyn[key] += c
    return g, dict(wyn)

def przewiduj(struk, q, g):
    """Dokladne przejscie p# -> q# z mechanizmu (bez przyblizen):
       kazda klasa reszt mod q zajeta przez punkty czlonu usuwa je w jednej kopii."""
    ee = 1 if g == 2 * q else 0
    out = defaultdict(int)
    for (j, ie, ii), c in struk.items():
        P = ee + ie + ii
        out[j] += c * (q - (j + 1) + P)             # kopie nietkniete
        sing = (j - 1) - (2 * ii + ie)              # pojedyncze punkty wewnetrzne
        if j >= 2 and sing > 0: out[j - 1] += c * sing
        if j >= 3 and ii > 0: out[j - 2] += c * ii  # PODWOJNE ZLANIE
    return {j: v for j, v in out.items() if v}
'''
with open('pary_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('pary_worker.py'), 'bajtow; koniec:', repr(open('pary_worker.py').read()[-30:]))

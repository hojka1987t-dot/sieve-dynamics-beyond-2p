# KOMORKA A - zapisuje workera (bez %%writefile). Uruchom, potem komorke B.
kod = r'''
from math import gcd
WERSJA = "4.1"

def generuj_pierwsze(n):
    pr = []; x = 2
    while len(pr) < n:
        if all(x % p for p in pr if p * p <= x): pr.append(x)
        x += 1
    return pr

def rozklad_csp(wezly, fale, g):
    """Dla jednego okna: ile przypisan klas fal endgame zostawia dokladnie m
    niepokrytych wezlow wewnetrznych (m = 0..N). Konce bezpieczne: klasy 0 i g
    zakazane. Spamietywanie po (indeks fali, maska niepokrytych)."""
    N = len(wezly); K = len(fale)
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
            v = [0] * (N + 1); v[bin(unc).count('1')] = 1; return v
        klucz = (i, unc); r = memo.get(klucz)
        if r is not None: return r
        acc = [0] * (N + 1)
        for m, kr in warstwy[i]:
            sub = f(i + 1, unc & ~m)
            for t, c in enumerate(sub):
                if c: acc[t] += kr * c
        memo[klucz] = acc; return acc
    return f(0, (1 << N) - 1)

def zadanie(args):
    """(k, r_base, g, v0_od, v0_do) -> (g, {j: n_{g,j} z tego zakresu okien})
    j = liczba luk w czlonie = 1 + liczba wewnetrznych liczb wzgl. pierwszych."""
    k, r_base, g, a, b = args
    pr = generuj_pierwsze(k); Pb = 1
    for p in pr[:r_base]: Pb *= p
    fale = pr[r_base:k]
    wynik = {}
    for v0 in range(a, b):
        if gcd(v0, Pb) != 1 or gcd(v0 + g, Pb) != 1: continue
        wez = [i for i in range(1, g) if gcd(v0 + i, Pb) == 1]
        for m, c in enumerate(rozklad_csp(wez, fale, g)):
            if c: wynik[m + 1] = wynik.get(m + 1, 0) + c
    return g, wynik
'''
with open('holt_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('holt_worker.py'), 'bajtow do', os.getcwd())
print('koniec pliku:', repr(open('holt_worker.py').read()[-22:]))

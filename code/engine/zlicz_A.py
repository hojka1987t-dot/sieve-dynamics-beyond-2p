# =====================================================================
# KOMORKA A - zapis workera. Uruchom, potem komorke B.
# =====================================================================
kod = r'''
WERSJA = "3.1"

from math import gcd


def generuj_pierwsze(n):
    pr = []
    x = 2
    while len(pr) < n:
        if all(x % p for p in pr if p * p <= x):
            pr.append(x)
        x += 1
    return pr


def zlicz_csp(wezly, fale, end_offset):
    """
    Liczy WSZYSTKIE pelne przypisania klas reszt pokrywajace wezly,
    z zachowaniem bezpieczenstwa koncow. Nieuzyte fale maja swoje
    bezpieczne klasy jako swobodne mnozniki.

    Spamietywanie po (indeks fali, maska niepokrytych): zamienia
    wykladniczosc w liczbie fal na wykladniczosc w liczbie wezlow.
    Przyspieszenie zmierzone: ~170x przy k=12.
    """
    N = len(wezly)
    if N == 0:
        m = 1
        for p in fale:
            m *= (p - 1) if end_offset % p == 0 else (p - 2)
        return m
    fl = list(fale)
    warstwy = []
    for p in fl:
        em = end_offset % p
        d = {}
        for i, w in enumerate(wezly):
            r = w % p
            if r != 0 and r != em:
                d[r] = d.get(r, 0) | (1 << i)
        grup = {}
        for r, m in d.items():
            grup[m] = grup.get(m, 0) + 1
        bezp = (p - 1) if em == 0 else (p - 2)
        puste = bezp - len(d)
        if puste > 0:
            grup[0] = grup.get(0, 0) + puste
        warstwy.append(sorted(grup.items()))

    memo = {}
    ogon = [1] * (len(fl) + 1)
    for j in range(len(fl) - 1, -1, -1):
        p = fl[j]
        ogon[j] = ogon[j + 1] * ((p - 1) if end_offset % p == 0 else (p - 2))

    def f(i, unc):
        if unc == 0:
            return ogon[i]
        if i == len(fl):
            return 0
        klucz = (i, unc)
        v = memo.get(klucz)
        if v is not None:
            return v
        s = 0
        for maska, krot in warstwy[i]:
            s += krot * f(i + 1, unc & ~maska)
        memo[klucz] = s
        return s

    return f(0, (1 << N) - 1)


def zadanie_L(args):
    """
    Dla jednej roznicy L: liczba WSZYSTKICH pokryc ograniczonych,
    czyli N_k(L) = liczba x mod P_k# zaczynajacych luke dlugosci L.
    Wielkosc NIEZALEZNA OD BAZY (baza to tylko sposob enumeracji).

    Kontrola poprawnosci: dla L = h(k) wynik musi rownac sie n_seq
    z pliku remainders.txt Zillera.
    """
    k, r_base, L, wezly_max = args
    pr = generuj_pierwsze(k)
    Pb = 1
    for p in pr[:r_base]:
        Pb *= p
    fale = pr[r_base:k]
    oc = [v for v in range(1, Pb + 1) if gcd(v, Pb) == 1]
    ocs = set(oc)
    tot = 0
    okien = 0
    for v0 in oc:
        w2 = v0 + L if v0 + L <= Pb else v0 + L - Pb
        if w2 not in ocs:
            continue
        wez = [i for i in range(1, L) if gcd(v0 + i, Pb) == 1]
        if wezly_max and len(wez) > wezly_max:
            return {'L': L, 'N': None, 'okien': okien, 'za_duzo': len(wez)}
        okien += 1
        tot += zlicz_csp(wez, fale, L)
    return {'L': L, 'N': tot, 'okien': okien, 'za_duzo': 0}
'''
with open('zlicz_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('zlicz_worker.py'), 'bajtow do', os.getcwd())
print('koniec pliku:', repr(open('zlicz_worker.py').read()[-20:]))

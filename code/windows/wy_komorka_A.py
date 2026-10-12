%%writefile wy_worker.py
# -*- coding: utf-8 -*-
"""
W_y = min |[0,y] bez sumy klas (a_p mod p), p <= z|
minimum po WSZYSTKICH wyborach klas reszt, po jednej na liczbe pierwsza.

Obciecie domyslne jak u Banksa-Forda-Tao (arXiv:1908.08613, wzor 1.11):
    z = (y / log y)^(1/2)

Metoda: branch and bound. Odcina galaz, gdy pozostale liczby pierwsze nie
moga juz poprawic najlepszego wyniku - to samo ograniczenie pojemnosciowe,
ktorego uzywa solve_csp. Wynik jest DOKLADNY, nie przyblizony.

Po co: gorne ograniczenie na W_y w (1.12) bierze sie z wyboru a_p = 0 dla
kazdej liczby pierwszej, czyli ze zwyklego kola. Hipoteza folklorystyczna
mowi, ze to gorne ograniczenie jest blizsze prawdy. Iloraz W_y/(a_p=0) jest
empiryczna trescia tej hipotezy.
"""
import math

WERSJA = "1.0"


def pierwsze_do(n):
    p = []
    x = 2
    while x <= n:
        if all(x % q for q in p if q * q <= x):
            p.append(x)
        x += 1
    return p


def _maski(P, n):
    return [[sum(1 << v for v in range(a, n, p)) for a in range(p)] for p in P]


def zadanie_galaz(args):
    """
    Jedna galaz: klasy dla pierwszych `len(prefiks)` liczb pierwszych sa
    ustalone, reszta przeszukiwana z odcinaniem. Zwraca (najlepsze, wezly).
    """
    y, P, prefiks, gorne = args
    n = y + 1
    pelna = (1 << n) - 1
    maski = _maski(P, n)
    gl = len(P)

    niepokryte = pelna
    for i, a in enumerate(prefiks):
        niepokryte &= ~maski[i][a]
    start = len(prefiks)

    naj = [gorne]
    najw = [None]
    wezly = [0]

    def dfs(i, niep, wybor):
        if naj[0] == 0:          # pelne pokrycie znalezione - lepiej byc nie moze
            return
        wezly[0] += 1
        u = niep.bit_count()
        if u >= naj[0]:
            moga = 0
            for j in range(i, gl):
                p = P[j]
                b = 0
                mj = maski[j]
                for a in range(p):
                    c = (niep & mj[a]).bit_count()
                    if c > b:
                        b = c
                moga += b
            if u - moga >= naj[0]:
                return
        if i == gl:
            if u < naj[0]:
                naj[0] = u
                najw[0] = tuple(prefiks) + tuple(wybor)
            return
        p = P[i]
        mi = maski[i]
        rz = sorted(range(p), key=lambda a: -(niep & mi[a]).bit_count())
        for a in rz:
            wybor.append(a)
            dfs(i + 1, niep & ~mi[a], wybor)
            wybor.pop()

    dfs(start, niepokryte, [])
    return naj[0], najw[0], wezly[0]


def trywialne(y, P):
    """Liczba ocalalych przy a_p = 0 dla kazdej liczby pierwszej (zwykle kolo)."""
    n = y + 1
    pk = 0
    for p in P:
        for v in range(0, n, p):
            pk |= 1 << v
    return ((1 << n) - 1 & ~pk).bit_count()

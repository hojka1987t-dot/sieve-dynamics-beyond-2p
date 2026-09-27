%%writefile roznice_worker.py
"""
Weryfikator brakujacych roznic - worker.
Sprawdza, czy dana roznica L wystepuje jako roznica miedzy kolejnymi
liczbami wzglednie pierwszymi z p_k#.

Metoda niezalezna od AGPA Zillera: enumeracja okien w kole bazowym
+ dokladne pokrycie falami endgame (CSP z przycinaniem pojemnosciowym).
"""
from math import gcd

WERSJA = "2.0"


class BudzetWyczerpany(Exception):
    pass


def generuj_pierwsze(n):
    pr = []; x = 2
    while len(pr) < n:
        if all(x % p for p in pr if p * p <= x):
            pr.append(x)
        x += 1
    return pr


_CACHE = {}


def ocaleli_bazy(r_base, primes, ogon):
    """Ocalali w jednym okresie kola bazowego + ogon dlugosci `ogon`."""
    P = 1
    for p in primes[:r_base]:
        P *= p
    if (r_base, ogon) in _CACHE:
        return _CACHE[(r_base, ogon)]
    sito = bytearray(b'\x01') * (P + 1)
    for p in primes[:r_base]:
        sito[p::p] = bytearray(len(range(p, P + 1, p)))
    sito[0] = 0
    oc = [i for i in range(1, P + 1) if sito[i]]
    del sito
    wyn = (oc + [P + s for s in oc if s <= ogon], P)
    _CACHE[(r_base, ogon)] = wyn
    return wyn


def _budowa(r_base, primes, target_copy):
    """Strumien luk dla sektora target_copy. Stala pamiec, bez tablic."""
    def base():
        yield 2

    def layer(p, P_prev, parent):
        inv = pow(P_prev, -1, p); cg = 0
        for copy in range(p):
            vm = 1 % p
            for g in parent():
                vm = (vm + g) % p
                k = (-vm * inv) % p
                cg += g
                if copy != k:
                    yield cg; cg = 0

    def targeted(p, P_prev, tc, parent):
        inv = pow(P_prev, -1, p); cg = 0; vm = 1 % p
        for g in parent():
            vm = (vm + g) % p
            k = (-vm * inv) % p
            cg += g
            if tc != k:
                yield cg; cg = 0

    P = 2; s = base
    for i in range(1, r_base - 1):
        p = primes[i]; cp = P
        def mk(a, b, c): return lambda: layer(a, b, c)
        s = mk(p, cp, s); P *= p
    top = primes[r_base - 1]
    def mkt(a, b, c, d): return lambda: targeted(a, b, c, d)
    return mkt(top, P, target_copy, s), P, P * top


def ocaleli_sektor(r_base, primes, c, ogon):
    """
    Generator wartosci bezwzglednych ocalalych w sektorze c, plus `ogon`
    jednostek dalej (okna przecinajace granice sektora). Pamiec stala.
    """
    top = primes[r_base - 1]
    strum, P_prev, _ = _budowa(r_base, primes, c)
    anchor = 1 + c * P_prev
    # dla dokladnie jednego sektora anchor jest podzielny przez top - nie jest ocalalym
    if anchor % top != 0:
        yield anchor
    v = anchor
    for g in strum():
        v += g
        yield v
    if ogon > 0:
        kres = 1 + (c + 1) * P_prev + ogon
        krok = 1
        while True:
            c2 = (c + krok) % top
            poczatek = 1 + (c + krok) * P_prev
            if poczatek > kres:
                break
            strum2, _, _ = _budowa(r_base, primes, c2)
            przes = poczatek - (1 + c2 * P_prev)
            v2 = 1 + c2 * P_prev
            for g in strum2():
                v2 += g
                w = v2 + przes
                if w > kres:
                    break
                yield w
            krok += 1


def solve_csp(wezly, fale, end_offset, budzet, licznik):
    """
    Czy istnieje przypisanie (fala -> jedna klasa reszt) wybijajace wszystkie
    wezly wewnetrzne i nie naruszajace zadnego z koncow?
    Zwraca (ok, przypisanie). Podnosi BudzetWyczerpany po przekroczeniu limitu.
    """
    if not wezly:
        return True, []
    N = len(wezly)
    cov = {p: {} for p in fale}
    nc = [[] for _ in range(N)]
    for p in fale:
        em = end_offset % p
        cp = cov[p]
        for i, w in enumerate(wezly):
            r = w % p
            if r != 0 and r != em:
                cp[r] = cp.get(r, 0) | (1 << i)
                nc[i].append((p, r))
    # dokladna pojemnosc dla tego okna - rygorystyczna, liczona z rzeczywistych pozycji
    poj = sum(max((m.bit_count() for m in d.values()), default=0) for d in cov.values())
    if N > poj:
        return False, []

    def dfs(unc, av, asg):
        licznik[0] += 1
        if licznik[0] > budzet:
            raise BudzetWyczerpany
        if unc == 0:
            return True, asg
        if not av:
            return False, []
        dyn = 0
        for p in av:
            b = 0
            for m in cov[p].values():
                c = (m & unc).bit_count()
                if c > b:
                    b = c
            dyn += b
        if unc.bit_count() > dyn:
            return False, []
        best = None; mn = 1 << 30; t = unc
        while t:
            l = t & -t; i = l.bit_length() - 1; t ^= l
            ch = [(p, r) for p, r in nc[i] if p in av]
            if not ch:
                return False, []
            if len(ch) < mn:
                mn = len(ch); best = ch
                if mn == 1:
                    break
        best.sort(key=lambda it: (cov[it[0]][it[1]] & unc).bit_count(), reverse=True)
        for p, r in best:
            ok, res = dfs(unc & ~cov[p][r], av - {p}, asg + [(p, r)])
            if ok:
                return True, res
        return False, []

    return dfs((1 << N) - 1, set(fale), [])


def algorytm_crt(reszty, moduly):
    s = 0; il = 1
    for m in moduly:
        il *= m
    for r, m in zip(reszty, moduly):
        q = il // m
        s += r * q * pow(q, -1, m)
    return s % il


def zloz_crt(v0, L, assignment, fale, P_base):
    reszty = []; moduly = []; uzyte = set()
    for p, r in assignment:
        uzyte.add(p)
        reszty.append((-(v0 + r) * pow(P_base, -1, p)) % p)
        moduly.append(p)
    for p in fale:
        if p in uzyte:
            continue
        sr = 1
        while sr == 0 or sr == (L % p):
            sr += 1
        reszty.append((-(v0 + sr) * pow(P_base, -1, p)) % p)
        moduly.append(p)
    return v0 + algorytm_crt(reszty, moduly) * P_base


def weryfikuj(V, L, P_target):
    """Czy V faktycznie zaczyna luke dlugosci L: oba konce wzgl. pierwsze, wnetrze wybite."""
    if V <= 0 or gcd(V, P_target) != 1 or gcd(V + L, P_target) != 1:
        return False
    for i in range(1, L):
        if gcd(V + i, P_target) == 1:
            return False
    return True


def zadanie_L(args):
    """
    Sprawdza roznice L w jednym sektorze kola bazowego, strumieniowo.
    Pamiec stala - nie powstaje zadna tablica ocalalych.
    rozstrzygniete: wspoldzielony slownik L -> True; jesli inny sektor
    znalazl juz swiadka dla tego L, ten konczy natychmiast.
    """
    k, r_base, L, budzet, sektor, _nieuzywane, rozstrzygniete = args
    od = sektor
    if rozstrzygniete is not None and L in rozstrzygniete:
        return {'L': L, 'k': k, 'r_base': r_base, 'od': sektor, 'do': None, 'okien': 0,
                'krokow': 0, 'budzet_przekroczony': False, 'wystepuje': False,
                'V': None, 'zweryfikowane': None, 'pominiete': True}
    primes = generuj_pierwsze(k)
    fale = primes[r_base:k]
    top = primes[r_base - 1]
    P_prev = 1
    for p in primes[:r_base - 1]:
        P_prev *= p
    P = P_prev * top
    koniec_sektora = 1 + (sektor + 1) * P_prev

    licznik = [0]; okien = 0
    przekroczono = False; swiadek = None

    # bufor przesuwny: wystarczy L//2+2 pozycji, bo najmniejsza luka to 2
    BUF = L // 2 + 4
    buf = [0] * BUF
    n = 0; ogon_idx = 0

    for v in ocaleli_sektor(r_base, primes, sektor, L):
        buf[n % BUF] = v
        n += 1
        if n < 2:
            continue
        # szukamy v0 = v - L wsrod wczesniejszych pozycji
        cel = v - L
        t = ogon_idx
        while t < n - 1 and buf[t % BUF] < cel:
            t += 1
        ogon_idx = t
        if t < n - 1 and buf[t % BUF] == cel:
            v0 = cel
            if v0 >= koniec_sektora:
                break                     # poczatek juz poza sektorem - to zadanie sasiada
            okien += 1
            wez = [buf[q % BUF] - v0 for q in range(t + 1, n - 1)]
            try:
                ok, asg = solve_csp(wez, fale, L, budzet, licznik)
            except BudzetWyczerpany:
                przekroczono = True
                ok, asg = False, []
                licznik[0] = 0
            if ok:
                swiadek = (v0, asg)
                if rozstrzygniete is not None:
                    rozstrzygniete[L] = True
                break

    P_target = 1
    for p in primes[:k]:
        P_target *= p

    wynik = {'L': L, 'k': k, 'r_base': r_base, 'od': od, 'do': None, 'okien': okien,
             'krokow': licznik[0], 'budzet_przekroczony': przekroczono,
             'wystepuje': swiadek is not None, 'V': None, 'zweryfikowane': None,
             'pominiete': False}
    if swiadek:
        v0, asg = swiadek
        V = zloz_crt(v0, L, asg, fale, P)
        wynik['V'] = V
        wynik['zweryfikowane'] = weryfikuj(V, L, P_target)
    return wynik

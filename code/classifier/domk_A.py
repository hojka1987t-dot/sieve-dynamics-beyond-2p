# KOMORKA A - zapis workera 6.1 (klasyfikator + domkniecie). Uruchom, potem komorke B.
kod = r'''"""
Klasyfikator brakujacych roznic - worker.
Sprawdza, czy dana roznica L wystepuje jako roznica miedzy kolejnymi
liczbami wzglednie pierwszymi z p_k#.

Metoda niezalezna od AGPA Zillera: enumeracja okien w kole bazowym
+ dokladne pokrycie falami endgame (CSP z przycinaniem pojemnosciowym).
"""
from math import gcd

WERSJA = "6.1"


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



def solve_csp_z(wezly, fale, zakazane, budzet, licznik):
    """Pokrycie wezlow falami; klasa fali nie moze trafic w zadna z pozycji
       'zakazane' (konce okna i punkt, ktory ma zostac wolny)."""
    if not wezly:
        return True, []
    N = len(wezly)
    cov = {p: {} for p in fale}
    nc = [[] for _ in range(N)]
    for p in fale:
        zk = {z % p for z in zakazane}
        cp = cov[p]
        for i, w in enumerate(wezly):
            r = w % p
            if r not in zk:
                cp[r] = cp.get(r, 0) | (1 << i)
                nc[i].append((p, r))
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
                if c > b: b = c
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
                if mn == 1: break
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



def zloz_crt_z(v0, zakazane, assignment, fale, P_base):
    reszty = []; moduly = []; uzyte = set()
    for p, r in assignment:
        uzyte.add(p)
        reszty.append((-(v0 + r) * pow(P_base, -1, p)) % p); moduly.append(p)
    for p in fale:
        if p in uzyte: continue
        zk = {z % p for z in zakazane}
        sr = 0
        while sr in zk: sr += 1
        reszty.append((-(v0 + sr) * pow(P_base, -1, p)) % p); moduly.append(p)
    return v0 + algorytm_crt(reszty, moduly) * P_base

def weryfikuj_konst(X, a, g, P_target):
    """Czy X, X+a, X+g sa kolejnymi liczbami wzgl. pierwszymi z P_target
       (czyli konstelacja (a, g-a) wystepuje w cyklu)."""
    if X <= 0: return False
    for i in range(0, g + 1):
        wp = gcd(X + i, P_target) == 1
        if wp != (i in (0, a, g)): return False
    return True

def zadanie_konst(args):
    """Czy konstelacja (a, g-a) wystepuje w G(p_k#)? Jeden sektor kola bazowego.
       Zabojstwo roznicy g przy nastepnej liczbie pierwszej q wymaga a = 2q."""
    k, r_base, g, a, budzet, sektor, rozstrz = args
    klucz = (k, g, a)
    if rozstrz is not None and klucz in rozstrz:
        return {'klucz': klucz, 'sektor': sektor, 'pominiete': True, 'okien': 0,
                'istnieje': False, 'budzet_przekroczony': False, 'X': None, 'zweryfikowane': None}
    primes = generuj_pierwsze(k)
    fale = primes[r_base:k]
    P_prev = 1
    for p in primes[:r_base - 1]: P_prev *= p
    P = P_prev * primes[r_base - 1]
    koniec = 1 + (sektor + 1) * P_prev
    licznik = [0]; okien = 0; przekr = False; swiadek = None
    BUF = g // 2 + 4; buf = [0] * BUF; n = 0; og = 0
    for v in ocaleli_sektor(r_base, primes, sektor, g):
        buf[n % BUF] = v; n += 1
        if n < 2: continue
        cel = v - g; t = og
        while t < n - 1 and buf[t % BUF] < cel: t += 1
        og = t
        if t < n - 1 and buf[t % BUF] == cel:
            v0 = cel
            if v0 >= koniec: break
            wez = [buf[qq % BUF] - v0 for qq in range(t + 1, n - 1)]
            if a not in wez: continue
            wez.remove(a); okien += 1
            try:
                ok, asg = solve_csp_z(wez, fale, (0, a, g), budzet, licznik)
            except BudzetWyczerpany:
                przekr = True; ok = False; licznik[0] = 0
            if ok:
                swiadek = (v0, asg)
                if rozstrz is not None: rozstrz[klucz] = True
                break
    P_target = 1
    for p in primes[:k]: P_target *= p
    w = {'klucz': klucz, 'sektor': sektor, 'pominiete': False, 'okien': okien,
         'istnieje': swiadek is not None, 'budzet_przekroczony': przekr, 'X': None, 'zweryfikowane': None}
    if swiadek:
        X = zloz_crt_z(swiadek[0], (0, a, g), swiadek[1], fale, P)
        w['X'] = X; w['zweryfikowane'] = weryfikuj_konst(X, a, g, P_target)
    return w


def weryfikuj_wolne(X, wolne, g, P_target):
    """Czy w [X, X+g] liczbami wzgl. pierwszymi z P_target sa dokladnie X, X+g i X+w dla w w 'wolne'."""
    if X <= 0: return False
    zb = set(wolne) | {0, g}
    for i in range(0, g + 1):
        if (gcd(X + i, P_target) == 1) != (i in zb): return False
    return True

def _okna(k, r_base, g, sektor):
    """Generator okien [v0, v0+g] o obu koncach ocalalych w kole bazowym (sektor), z wezlami."""
    primes = generuj_pierwsze(k)
    P_prev = 1
    for p in primes[:r_base - 1]: P_prev *= p
    koniec = 1 + (sektor + 1) * P_prev
    BUF = g // 2 + 4; buf = [0] * BUF; n = 0; og = 0
    for v in ocaleli_sektor(r_base, primes, sektor, g):
        buf[n % BUF] = v; n += 1
        if n < 2: continue
        cel = v - g; t = og
        while t < n - 1 and buf[t % BUF] < cel: t += 1
        og = t
        if t < n - 1 and buf[t % BUF] == cel:
            v0 = cel
            if v0 >= koniec: return
            yield v0, [buf[qq % BUF] - v0 for qq in range(t + 1, n - 1)]

def _swiadek(k, r_base, g, wolne, v0, asg):
    primes = generuj_pierwsze(k)
    fale = primes[r_base:k]
    P = 1
    for p in primes[:r_base]: P *= p
    Pt = 1
    for p in primes[:k]: Pt *= p
    zak = (0, g) + tuple(wolne)
    X = zloz_crt_z(v0, zak, asg, fale, P)
    return X, weryfikuj_wolne(X, wolne, g, Pt)

def zadanie_wolne(args):
    """Czy w G(p_k#) wystepuje czlon rozpietosci g, ktorego JEDYNYMI punktami
       wewnetrznymi sa 'wolne'? (np. trojka (u, 2q, w): wolne = (u, u+2q))"""
    k, r_base, g, wolne, budzet, sektor, rozstrz = args
    klucz = (k, g, tuple(wolne))
    if rozstrz is not None and klucz in rozstrz:
        return {'pominiete': True, 'istnieje': False, 'budzet_przekroczony': False, 'okien': 0}
    fale = generuj_pierwsze(k)[r_base:k]
    licznik = [0]; okien = 0; przekr = False
    for v0, wez in _okna(k, r_base, g, sektor):
        if any(w not in wez for w in wolne): continue
        okien += 1
        wz = [w for w in wez if w not in wolne]
        try:
            ok, asg = solve_csp_z(wz, fale, (0, g) + tuple(wolne), budzet, licznik)
        except BudzetWyczerpany:
            przekr = True; ok = False; licznik[0] = 0
        if ok:
            if rozstrz is not None: rozstrz[klucz] = True
            X, wer = _swiadek(k, r_base, g, wolne, v0, asg)
            return {'pominiete': False, 'istnieje': True, 'X': X, 'zweryfikowane': wer,
                    'wolne': tuple(wolne), 'budzet_przekroczony': przekr, 'okien': okien}
    return {'pominiete': False, 'istnieje': False, 'budzet_przekroczony': przekr, 'okien': okien}

def zadanie_para(args):
    """Czy g jest suma dwoch SASIEDNICH luk (t, g-t) w G(p_k#), z t w [t_min, t_max]
       i t, g-t spoza 'wyklucz'? Jedno przejscie strumienia, wszystkie t naraz."""
    k, r_base, g, t_min, t_max, wyklucz, budzet, sektor, rozstrz = args
    klucz = (k, g, 'para')
    if rozstrz is not None and klucz in rozstrz:
        return {'pominiete': True, 'istnieje': False, 'budzet_przekroczony': False, 'okien': 0}
    fale = generuj_pierwsze(k)[r_base:k]
    licznik = [0]; okien = 0; przekr = False
    for v0, wez in _okna(k, r_base, g, sektor):
        kand = [t for t in wez if t_min <= t <= t_max and t not in wyklucz and (g - t) not in wyklucz]
        if not kand: continue
        okien += 1
        for t in kand:
            wz = [w for w in wez if w != t]
            try:
                ok, asg = solve_csp_z(wz, fale, (0, t, g), budzet, licznik)
            except BudzetWyczerpany:
                przekr = True; ok = False; licznik[0] = 0
            if ok:
                if rozstrz is not None: rozstrz[klucz] = True
                X, wer = _swiadek(k, r_base, g, (t,), v0, asg)
                return {'pominiete': False, 'istnieje': True, 'X': X, 'zweryfikowane': wer,
                        'wolne': (t,), 'budzet_przekroczony': przekr, 'okien': okien}
    return {'pominiete': False, 'istnieje': False, 'budzet_przekroczony': przekr, 'okien': okien}
'''
with open('klas_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('klas_worker.py'), 'bajtow; koniec:', repr(open('klas_worker.py').read()[-40:]))

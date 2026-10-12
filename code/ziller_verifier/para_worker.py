"""Celowane wyszukiwanie swiadka-PARY dla luki L na etapie k: luka L w G(p_k#), ktorej wnetrze na etapie k-1
ma dokladnie jeden punkt u (usuwany przez q = p_k). Korzysta z weryfikatora roznice_worker (strumien, baza r_base)."""
from math import gcd, prod
import roznice_worker as W

class Budzet(Exception): pass

def csp_z_zakazem(wezly, fale, zakazane, budzet, licznik):
    # jak W.solve_csp, ale klasy trafiajace w ktorykolwiek punkt z 'zakazane' (konce i u) sa wykluczone
    if not wezly: return True, []
    N = len(wezly); cov = {p: {} for p in fale}; nc = [[] for _ in range(N)]
    for p in fale:
        zr = {z % p for z in zakazane}
        for i, w in enumerate(wezly):
            r = w % p
            if r not in zr:
                cov[p][r] = cov[p].get(r, 0) | (1 << i); nc[i].append((p, r))
    if N > sum(max((m.bit_count() for m in d.values()), default=0) for d in cov.values()): return False, []
    def dfs(unc, av, asg):
        licznik[0] += 1
        if licznik[0] > budzet: raise Budzet
        if unc == 0: return True, asg
        if not av: return False, []
        if unc.bit_count() > sum(max(((m & unc).bit_count() for m in cov[p].values()), default=0) for p in av): return False, []
        best = None; mn = 1 << 30; t = unc
        while t:
            l = t & -t; i = l.bit_length() - 1; t ^= l
            ch = [(p, r) for p, r in nc[i] if p in av]
            if not ch: return False, []
            if len(ch) < mn:
                mn = len(ch); best = ch
                if mn == 1: break
        best.sort(key=lambda it: (cov[it[0]][it[1]] & unc).bit_count(), reverse=True)
        for p, r in best:
            ok, res = dfs(unc & ~cov[p][r], av - {p}, asg + [(p, r)])
            if ok: return True, res
        return False, []
    return dfs((1 << N) - 1, set(fale), [])

def csp_jeden_wolny(wezly, fale, L, q, budzet, licznik):
    """Przypisanie (p -> klasa) dla p w fale, ktore pokrywa wszystkie wezly oprocz DOKLADNIE jednego u,
    nie trafia w konce 0, L ani w u; u musi spelniac u mod q not in {0, L mod q}. Zwraca (u, przypisanie) lub None."""
    N = len(wezly); cov = {p: {} for p in fale}; nc = [[] for _ in range(N)]
    for p in fale:
        e = {0, L % p}
        for i, w in enumerate(wezly):
            r = w % p
            if r not in e:
                cov[p][r] = cov[p].get(r, 0) | (1 << i); nc[i].append((p, r))
    dozw_u = 0
    for i, w in enumerate(wezly):
        if w % q not in (0, L % q): dozw_u |= 1 << i
    def dfs(unc, av, asg, u):
        licznik[0] += 1
        if licznik[0] > budzet: raise Budzet
        if unc == 0: return (u, asg) if u is not None else None
        if u is None and unc.bit_count() == 1 and (unc & dozw_u): return (unc.bit_length() - 1, asg)
        if not av: return None
        zap = sum(max(((m & unc).bit_count() for m in cov[p].values() if not (u is not None and m >> u & 1)), default=0) for p in av)
        if unc.bit_count() - (1 if u is None else 0) > zap: return None
        best = None; mn = 1 << 30; t = unc; bi = None
        while t:
            l = t & -t; i = l.bit_length() - 1; t ^= l
            ch = [(p, r) for p, r in nc[i] if p in av and not (u is not None and cov[p][r] >> u & 1)]
            if not ch and (u is not None or not (dozw_u >> i & 1)): return None
            if len(ch) < mn: mn = len(ch); best = ch; bi = i
            if mn <= 1: break
        best.sort(key=lambda it: (cov[it[0]][it[1]] & unc).bit_count(), reverse=True)
        for p, r in best:
            res = dfs(unc & ~cov[p][r], av - {p}, asg + [(p, r)], u)
            if res: return res
        if u is None and (dozw_u >> bi & 1):                       # galaz: wezel bi zostaje wolny (to jest u)
            return dfs(unc & ~(1 << bi), av, asg, bi)
        return None
    return dfs((1 << N) - 1, set(fale), [], None)

def para_sektor(args):
    k, L, r_base, sektor, budzet = args
    primes = W.generuj_pierwsze(k); q = primes[k - 1]; fale = primes[r_base:k - 1]
    top = primes[r_base - 1]; P_prev = prod(primes[:r_base - 1]); P = P_prev * top
    koniec = 1 + (sektor + 1) * P_prev; BUF = L // 2 + 4; buf = [0] * BUF; n = 0; t0 = 0
    licznik = [0]; okien = 0; przekroczono = False
    for v in W.ocaleli_sektor(r_base, primes, sektor, L):
        buf[n % BUF] = v; n += 1
        if n < 2: continue
        cel = v - L; t = t0
        while t < n - 1 and buf[t % BUF] < cel: t += 1
        t0 = t
        if not (t < n - 1 and buf[t % BUF] == cel): continue
        v0 = cel
        if v0 >= koniec: break
        okien += 1; wez = [buf[j % BUF] - v0 for j in range(t + 1, n - 1)]
        try:
            res = csp_jeden_wolny(wez, fale, L, q, budzet, licznik)
        except Budzet:
            przekroczono = True; licznik[0] = 0; continue
        if res:
            ui, asg = res; u = wez[ui]
            V = W.zloz_crt(v0, L, asg + [(q, u % q)], fale + [q], P)
            return {'k': k, 'L': L, 'sektor': sektor, 'V': V, 'okien': okien, 'budzet_przekroczony': przekroczono}
    return {'k': k, 'L': L, 'sektor': sektor, 'V': None, 'okien': okien, 'budzet_przekroczony': przekroczono}

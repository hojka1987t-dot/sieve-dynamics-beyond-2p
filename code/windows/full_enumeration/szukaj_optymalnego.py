"""Czy wsrod OKIEN OPTYMALNYCH bazy r (W_r ocalalych na [0,y]) istnieje okno, ktorego
najliczniejsza klasa mod q ma >= cel wezlow?  Przeszukiwanie z odcieciami:
 (1) okno nie moze juz zejsc do W_r  (u - pojemnosc > W_r),
 (2) zadna klasa mod q nie ma juz >= cel wezlow (klasy moga tylko malec)."""
import sys, time

def pierwsze_do(z): return [p for p in range(2, z + 1) if all(p % d for d in range(2, int(p ** .5) + 1))]

def szukaj(z0, q, y, Wr, cel, limit_s=250):
    P = pierwsze_do(z0); n = y + 1; pelne = (1 << n) - 1
    maski = [[sum(1 << v for v in range(a, n, p)) for a in range(p)] for p in P]
    qm = [sum(1 << v for v in range(b, n, q)) for b in range(q)]
    t0 = time.time(); wezly = [0]; wynik = [None]
    def dfs(i, niep, wybor):
        if wynik[0] is not None: return
        wezly[0] += 1
        if wezly[0] % 200000 == 0 and time.time() - t0 > limit_s: raise TimeoutError
        u = niep.bit_count()
        if max((niep & m).bit_count() for m in qm) < cel: return            # odciecie (2)
        if i == len(P):
            if u == Wr: wynik[0] = list(wybor)
            return
        moga = 0
        for k in range(i, len(P)):
            moga += max((niep & m).bit_count() for m in maski[k])
        if u - moga > Wr: return                                             # odciecie (1)
        rz = sorted(range(P[i]), key=lambda a: -(niep & maski[i][a]).bit_count())
        for a in rz:
            dfs(i + 1, niep & ~maski[i][a], wybor + [a])
            if wynik[0] is not None: return
    try:
        dfs(0, pelne, [])
        return ('ZNALEZIONE' if wynik[0] else 'BRAK'), wezly[0], time.time() - t0, wynik[0]
    except TimeoutError:
        return 'LIMIT', wezly[0], time.time() - t0, None

if __name__ == '__main__':
    z0, q, y, Wr, Wn = map(int, sys.argv[1:6])
    st, w, t, wyb = szukaj(z0, q, y, Wr, Wr - Wn)
    print('z %d -> %d, y=%d, W_r=%d, W_r+1=%d, potrzebna klasa >= %d: %s (%d wezlow, %.1f s)' % (z0, q, y, Wr, Wn, Wr - Wn, st, w, t))
    if wyb: print('  wybor:', wyb)

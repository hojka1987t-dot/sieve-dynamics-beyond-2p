import multiprocessing
import math
import time
import importlib
import itertools
import wy_worker as W

importlib.reload(W)
if getattr(W, "WERSJA", "0") < "1.0":
    raise ImportError("wy_worker.py na dysku to stara wersja albo uciety plik.")


def policz_Wy(y, z=None, watki=None, glebokosc_podzialu=None, gadatliwy=True):
    """
    Zwraca (W_y, trywialne, najlepszy wybor klas). Wynik DOKLADNY.
    glebokosc_podzialu: na ilu pierwszych liczbach pierwszych rozbic na zadania
                        (None = dobierz tak, by bylo >= 4x liczba rdzeni)
    """
    if z is None:
        z = (y / math.log(y)) ** 0.5
    if watki is None:
        watki = multiprocessing.cpu_count()
    P = W.pierwsze_do(int(z))
    if not P:
        return y + 1, y + 1, ()

    triv = W.trywialne(y, P)

    if glebokosc_podzialu is None:
        m, il = 0, 1
        while m < len(P) - 1 and il < watki * 4:
            il *= P[m]
            m += 1
        glebokosc_podzialu = m
    prefiksy = list(itertools.product(*[range(p) for p in P[:glebokosc_podzialu]]))

    if gadatliwy:
        print("W_y | y=%d  z=%.1f  p<=%d (%d szt.)  a_p=0 daje %d  zadan=%d"
              % (y, z, P[-1], len(P), triv, len(prefiksy)))

    t0 = time.time()
    naj, najw, wezly = triv, None, 0
    zad = [(y, P, pre, triv) for pre in prefiksy]
    with multiprocessing.Pool(watki) as pool:
        zrob = 0
        for w, wyb, wz in pool.imap_unordered(W.zadanie_galaz, zad, chunksize=1):
            zrob += 1
            wezly += wz
            if w < naj:
                naj, najw = w, wyb
            if gadatliwy and zrob % max(1, len(zad) // 5) == 0:
                print("   %d/%d galezi, biezace min=%d, %.0f s"
                      % (zrob, len(zad), naj, time.time() - t0))
    if gadatliwy:
        print("  W_%d = %d   (a_p=0 daje %d, iloraz %.4f)  wezlow=%d  %.1f s"
              % (y, naj, triv, naj / triv, wezly, time.time() - t0))
    return naj, triv, najw


def tabela_Wy(lista_y, z=None, watki=None):
    """Jeden przekroj: zmienne y, obciecie domyslne z = (y/log y)^(1/2)."""
    print("=" * 76)
    print("W_y  (obciecie z = (y/log y)^(1/2), jak u Banks-Ford-Tao)")
    print("=" * 76)
    print("      y     z   ile p    W_y   a_p=0   iloraz      r      czas")
    wyn = []
    for y in lista_y:
        t = time.time()
        zz = z if z is not None else (y / math.log(y)) ** 0.5
        Wv, triv, _ = policz_Wy(y, z=zz, watki=watki, gadatliwy=False)
        P = W.pierwsze_do(int(zz))
        r = math.log(y) / math.log(zz)
        print("  %7d %5.1f   %4d  %6d  %6d   %.4f  %5.2f  %7.1f s"
              % (y, zz, len(P), Wv, triv, Wv / triv, r, time.time() - t))
        wyn.append((y, zz, len(P), Wv, triv, Wv / triv, r))
    return wyn


def siatka_Wy(lista_y, lista_z, watki=None, plik="wy_siatka.txt"):
    """
    SIATKA: dla kazdej pary (y, z) liczy W_y.

    Sens: obciecie BFT z = (y/log y)^(1/2) trzyma r = log y / log z prawie
    stale (~2.6-2.8), wiec wzdluz osi y iloraz jest plaski. Cala zmiennosc
    siedzi na osi z. Granville ("Sieving intervals and Siegel zeros",
    Acta Arith. 205 (2022)) wskazuje prog przy r = 2.

    Pytanie: czy iloraz zalezy glownie od r, czy osobno od y i liczby
    liczb pierwszych? Jesli punkty o tym samym r daja ten sam iloraz
    niezaleznie od y - zaleznosc jest jednoparametrowa.

    Wyniki dopisywane do pliku po kazdym punkcie, wiec przerwanie nic nie kasuje.
    """
    print("=" * 78)
    print("SIATKA W_y:  %d wartosci y x %d wartosci z" % (len(lista_y), len(lista_z)))
    print("=" * 78)
    print("      y     z  ile p       r     W_y   a_p=0   iloraz      czas")
    wyn = []
    with open(plik, "a") as f:
        f.write("# y z ile_p r W_y trywialne iloraz czas\
")
    for y in lista_y:
        for z in lista_z:
            if z >= y:
                continue
            t = time.time()
            P = W.pierwsze_do(z)
            if not P:
                continue
            Wv, triv, _ = policz_Wy(y, z=z, watki=watki, gadatliwy=False)
            r = math.log(y) / math.log(z)
            dt = time.time() - t
            print("  %7d %5d   %4d   %5.2f  %6d  %6d   %.4f  %7.1f s"
                  % (y, z, len(P), r, Wv, triv, Wv / triv, dt))
            wyn.append((y, z, len(P), r, Wv, triv, Wv / triv))
            with open(plik, "a") as f:
                f.write("%d %d %d %.4f %d %d %.6f %.1f\
"
                        % (y, z, len(P), r, Wv, triv, Wv / triv, dt))
    print()
    print("  zapisane do %s" % plik)
    print()
    print("  KONTROLA JEDNOPARAMETROWOSCI: punkty o zblizonym r, rozne y")
    wyn.sort(key=lambda t: t[3])
    for i in range(1, len(wyn)):
        a, b = wyn[i - 1], wyn[i]
        if abs(a[3] - b[3]) < 0.06 and a[0] != b[0]:
            print("    r=%.2f: y=%d -> %.4f | y=%d -> %.4f   (roznica %.4f)"
                  % (b[3], a[0], a[6], b[0], b[6], abs(a[6] - b[6])))
    return wyn


print("Zaladowano.")
print("  jeden przekroj:  wyn = tabela_Wy([1000,2000,5000,10000])")
print("  SIATKA (zalecane): wyn = siatka_Wy([1000,2000,4000,8000], [7,11,13,17,19,23,29])")

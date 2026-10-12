# Komorka C - nocny przebieg W_y (pazdziernik 2026)
# Wymaga wczesniejszego uruchomienia komorek A i B w tym samym kernelu.
# Kazdy punkt jest zapisywany od razu; punkty juz obecne w pliku sa pomijane,
# wiec po przerwaniu wystarczy uruchomic nocny() ponownie.
import os, time, math, datetime

PLIK = "wy_nocny.txt"
PLIK_WYBORY = "wy_nocny_wybory.txt"   # optymalne klasy reszt a_p dla kazdego punktu

# (y, z, oczekiwane W_y albo None) - od najtanszych
PLAN = [
    # kontrola zgodnosci z wynikami z wrzesnia
    (4000, 29, 614),
    (16000, 29, 2500),
    # kontrola z opublikowanymi wartosciami Granville'a i Lumleya
    # (ich przedzial (x, x+y] ma y liczb, nasz [0, y] - y+1, stad y-1)
    (339, 11, 68), (499, 17, 84), (1419, 19, 234),
    # seria przy u = log y / log z bliskim 2 - unormowane minimum przy u = 2
    # to stala c_- = sigma_-(2) z hipotezy o najwiekszych przerwach
    # (Granville-Lumley, arXiv:2009.05000); y = 1000 i 4000 juz policzone
    (2000, 41, None), (2000, 43, None), (2000, 47, None),
    (3000, 47, None), (3000, 53, None), (3000, 59, None),
    # y = 32000 - wydluzenie osi y (tempo zbieznosci)
    (32000, 7, None), (32000, 11, None), (32000, 13, None), (32000, 17, None),
    (32000, 19, None), (32000, 23, None), (32000, 29, None), (32000, 31, None),
    # y = 8000 - druga seria przy r = 2.3-2.5
    (8000, 37, None), (8000, 41, None), (8000, 43, None), (8000, 47, None),
    # y = 16000 - trzecia seria; ostatni punkt opcjonalny
    (16000, 41, None), (16000, 43, None), (16000, 47, None),
]


def _zrobione():
    zr = {}
    if os.path.exists(PLIK):
        for l in open(PLIK):
            if l.startswith("#") or not l.strip():
                continue
            c = l.split()
            zr[(int(c[0]), int(c[1]))] = int(c[4])
    return zr


def nocny(plan=None):
    plan = PLAN if plan is None else plan
    zr = _zrobione()
    if not os.path.exists(PLIK):
        with open(PLIK, "w") as f:
            f.write("# y z ile_p r W_y trywialne iloraz czas_s data\n")
    t_all = time.time()
    for y, z, ocz in plan:
        if (y, z) in zr:
            print("  (%d,%d) juz policzone: W_y=%d - pomijam" % (y, z, zr[(y, z)]))
            continue
        t = time.time()
        Wv, triv, wyb = policz_Wy(y, z=z, gadatliwy=False)
        dt = time.time() - t
        P = W.pierwsze_do(z)
        r = math.log(y) / math.log(z)
        with open(PLIK, "a") as f:
            f.write("%d %d %d %.4f %d %d %.6f %.1f %s\n"
                    % (y, z, len(P), r, Wv, triv, Wv / triv, dt,
                       datetime.datetime.now().isoformat(timespec="seconds")))
        with open(PLIK_WYBORY, "a") as f:
            # wyb: krotka klas a_p dla kolejnych liczb pierwszych <= z;
            # None znaczy, ze optimum osiaga zwykle kolo (a_p = 0 dla kazdego p)
            f.write("%d %d %d %s\n" % (y, z, Wv, "a_p=0" if wyb is None
                    else ",".join("%d:%d" % (p, a) for p, a in zip(P, wyb))))
        status = ""
        if ocz is not None:
            status = "  KONTROLA OK" if Wv == ocz else "  !!! KONTROLA NIEZGODNA (oczekiwane %d)" % ocz
        print("  %6d %4d  r=%.2f  W_y=%6d  a_p=0=%6d  iloraz=%.4f  %8.1f s%s"
              % (y, z, r, Wv, triv, Wv / triv, dt, status))
        if ocz is not None and Wv != ocz:
            print("Przerywam: wynik kontrolny nie zgadza sie z wrzesniowym.")
            return
    print("Gotowe. Laczny czas: %.2f h. Wyniki w %s" % ((time.time() - t_all) / 3600, PLIK))


print("Plan nocny: %d punktow. Uruchom:  nocny()" % len(PLAN))

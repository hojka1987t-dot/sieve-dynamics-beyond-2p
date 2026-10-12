# Komorka T - TEST PRAWA "+1" PRZY WYZSZYCH BAZACH (pazdziernik 2026)
# Wymaga wczesniejszego uruchomienia komorek A (nowa wersja) i B (W_y) w tym samym kernelu
# oraz pliku profil_z61.txt (z poprzedniej nocy) w folderze notatnika.
#
# Dla kazdego przejscia z_stare -> z_nowe:
#  1) profil nowej bazy: profil_z{z}.txt  ("y W wybor"), wznawialny;
#  2) dla KAZDEJ dlugosci y: przodek zwroconego optimum w starej bazie i jego odleglosc j od optimum;
#  3) jesli j >= 2: ukierunkowane przeszukiwanie, czy istnieje okno starej bazy z j <= 1 dajace to samo
#     optimum (remis). Brak takiego okna = PRAWDZIWE ZLAMANIE prawa "+1".
# Wyniki: test_plus1_wyniki.txt (dopisywane na biezaco), podsumowanie na ekranie.
import os, time

PLAN_TESTU = [(61, 67, 150), (67, 71, 172), (71, 73, 188), (73, 79, 198)]  # (z_stare, z_nowe, h(r+1)-2)
Y_DO = 700
LIMIT_PRZESZUKIWANIA_S = 900          # na jeden przypadek "j >= 2"
PLIK_WYNIKOW = "test_plus1_wyniki.txt"


def _pierwsze_do(z):
    return [p for p in range(2, z + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def _dane(nazwa, *podfoldery):
    """Plik danych: najpierw w biezacym folderze, potem w data/ archiwum (uruchamianie z code/<folder>)."""
    import os
    for p in (nazwa, os.path.join('..', '..', 'data', *podfoldery, nazwa)):
        if os.path.exists(p):
            return p
    return nazwa


def _wczytaj_profil(z):
    W = {}; wyb = {}
    for l in open(_dane("profil_z%d.txt" % z, "windows", "profiles")):
        if not l.strip():
            continue
        y, w, s = l.split()
        W[int(y)] = int(w); wyb[int(y)] = None if s == "-" else [int(t) for t in s.split(",")]
    return W, wyb


def _profil(z, y_od, y_do):
    plik = "profil_z%d.txt" % z
    zrobione = set()
    if os.path.exists(plik):
        for l in open(plik):
            if l.strip():
                zrobione.add(int(l.split()[0]))
    t0 = time.time(); n = 0
    with open(plik, "a") as f:
        for y in range(y_od, y_do + 1, 2):
            if y in zrobione:
                continue
            w, _, wyb = policz_Wy(y, z=z, gadatliwy=False)
            f.write("%d %d %s\n" % (y, w, ",".join(map(str, wyb)) if wyb is not None else "-"))
            f.flush(); n += 1
            if n % 25 == 0:
                print("  profil z=%d: y=%d, W=%d, %.0f s" % (z, y, w, time.time() - t0), flush=True)
    print("  profil z=%d gotowy (dopisano %d dlugosci, %.0f s)" % (z, n, time.time() - t0), flush=True)


def szukaj_przodka(z0, q, y, Wr, Wn, jmax=1, limit_s=LIMIT_PRZESZUKIWANIA_S):
    """Czy istnieje okno [0,y] bazy z0 z liczba ocalalych c <= Wr+jmax,
    ktorego najliczniejsza klasa mod q ma >= c - Wn wezlow?  -> 'ZNALEZIONE' / 'BRAK' / 'LIMIT'"""
    P = _pierwsze_do(z0); n = y + 1; pelne = (1 << n) - 1
    maski = [[sum(1 << v for v in range(a, n, p)) for a in range(p)] for p in P]
    qm = [sum(1 << v for v in range(b, n, q)) for b in range(q)]
    cel_min = Wr - Wn; t0 = time.time(); licz = [0]; wynik = [None]

    def dfs(i, niep):
        if wynik[0] is not None:
            return
        licz[0] += 1
        if licz[0] % 100000 == 0 and time.time() - t0 > limit_s:
            raise TimeoutError
        mk = max((niep & m).bit_count() for m in qm)
        if mk < cel_min:
            return                                   # klasy moga tylko malec
        u = niep.bit_count()
        if i == len(P):
            if u <= Wr + jmax and mk >= u - Wn:
                wynik[0] = u - Wr
            return
        moga = 0
        for k in range(i, len(P)):
            moga += max((niep & m).bit_count() for m in maski[k])
        if u - moga > Wr + jmax:
            return
        for a in sorted(range(P[i]), key=lambda a: -(niep & maski[i][a]).bit_count()):
            dfs(i + 1, niep & ~maski[i][a])
            if wynik[0] is not None:
                return
    try:
        dfs(0, pelne)
        return ("ZNALEZIONE" if wynik[0] is not None else "BRAK"), time.time() - t0
    except TimeoutError:
        return "LIMIT", time.time() - t0


def _test_przejscia(z0, z1, y_od):
    W0, _ = _wczytaj_profil(z0); W1, wyb1 = _wczytaj_profil(z1)
    P1 = _pierwsze_do(z1); P0 = [p for p in P1 if p <= z0]
    licz = {}; flagi = []
    for y in sorted(W1):
        if y < y_od or y not in W0:
            continue
        a = dict(zip(P1, wyb1[y])) if wyb1[y] is not None else {p: 0 for p in P1}
        S0 = [n for n in range(y + 1) if all(n % p != a[p] for p in P0)]
        j = len(S0) - W0[y]
        licz[j] = licz.get(j, 0) + 1
        if j >= 2:
            flagi.append(y)
    wynik_flag = []
    for y in flagi:
        st, t = szukaj_przodka(z0, z1, y, W0[y], W1[y])
        wynik_flag.append((y, W0[y], W1[y], st, t))
        print("    y=%d (W_stare=%d, W_nowe=%d): przodek z j<=1 -> %s (%.0f s)" % (y, W0[y], W1[y], st, t), flush=True)
    return licz, wynik_flag


def test_plus1():
    t_start = time.time()
    for z0, z1, y_od in PLAN_TESTU:
        if not os.path.exists("profil_z%d.txt" % z0):
            print("BRAK pliku profil_z%d.txt - przerwano przed przejsciem %d -> %d" % (z0, z0, z1)); return
        print("=== przejscie z=%d -> z=%d ===" % (z0, z1), flush=True)
        _profil(z1, y_od, Y_DO)
        licz, flagi = _test_przejscia(z0, z1, y_od)
        zlamania = [f for f in flagi if f[3] == "BRAK"]; limity = [f for f in flagi if f[3] == "LIMIT"]
        linia = ("%d -> %d: dlugosci %d | przodek optymalny %d, +1 %d, +2 i wiecej %d | z tego remisy %d, "
                 "ZLAMANIA %d, nierozstrzygniete %d" % (z0, z1, sum(licz.values()), licz.get(0, 0), licz.get(1, 0),
                 sum(v for k, v in licz.items() if k >= 2), len(flagi) - len(zlamania) - len(limity),
                 len(zlamania), len(limity)))
        print(linia, flush=True)
        with open(PLIK_WYNIKOW, "a") as f:
            f.write(linia + "\n")
            for y, a, b, st, t in flagi:
                f.write("   y=%d W_stare=%d W_nowe=%d -> %s\n" % (y, a, b, st))
    print("Gotowe. Laczny czas: %.1f h. Wyniki: %s" % ((time.time() - t_start) / 3600, PLIK_WYNIKOW))


print("Plan testu prawa +1: przejscia %s, dlugosci do %d. Uruchom:  test_plus1()"
      % (", ".join("%d->%d" % (a, b) for a, b, _ in PLAN_TESTU), Y_DO))

# KOMORKA C (dowolny etap) - n_{g,j}(p_K#) dla wybranych luk. Wymaga komorki A (holt_A_45.py -> holt_worker.py).
# Zapis po kazdej luce do PLIK: przebieg mozna przerwac i wznowic.
# Etapy (modele Holta z p0 = p_K wazne dla g < 2 * nastepna liczba pierwsza):
#   K=16 (53#): g <= 116    K=17 (59#): 118-120    K=18 (61#): 122-132    K=19 (67#): 134-140
#   K=20 (71#): 142-144     K=21 (73#): 146-156    K=22 (79#): 158-164    K=23 (83#): 166-176
# BAZA = liczba liczb pierwszych w kole bazowym: 5 (11#) - dobry wybor dla 16 rdzeni; 4 (7#) daje za malo okien.
import os, time, csv, multiprocessing, importlib
import holt_worker as HW
importlib.reload(HW)

K, BAZA = 17, 5                                   # G(59#), kolo bazowe 11#
LUKI = [20, 118, 120]                             # 20 = kontrola (nG47 + kroki jednorodne)
PLIK = "nG%d_nowe.csv" % HW.generuj_pierwsze(K)[-1]
KAWALKI = 256                                     # wiecej kawalkow niz rdzeni: rowniejsze obciazenie


def _gotowe():
    d = set()
    if os.path.exists(PLIK):
        for r in csv.reader(open(PLIK, encoding="utf-8")):
            if r and r[0].startswith("Gap Sum"):
                d.add(int(r[0].split("=")[1]))
    return d


def _jedna_luka(g, watki=None):
    pr = HW.generuj_pierwsze(K); Pb = 1
    for p in pr[:BAZA]: Pb *= p
    krok = max(1, Pb // KAWALKI)
    zad = [(K, BAZA, g, a, min(a + krok, Pb + 1)) for a in range(1, Pb + 1, krok)]
    wyn = {}; t0 = time.time(); zrob = 0
    with multiprocessing.Pool(watki or multiprocessing.cpu_count()) as pool:
        for _, w in pool.imap_unordered(HW.zadanie, zad):
            for j, c in w.items(): wyn[j] = wyn.get(j, 0) + c
            zrob += 1
            if zrob % 32 == 0:
                print("     luka %d: %d/%d kawalkow, %.1f min" % (g, zrob, len(zad), (time.time() - t0) / 60), flush=True)
    return wyn


def licz(watki=None):
    gotowe = _gotowe()
    for g in LUKI:
        if g in gotowe:
            print("luka %d juz policzona" % g); continue
        t0 = time.time(); print("luka %d ..." % g, flush=True)
        w = _jedna_luka(g, watki)
        jmax = max(w) if w else 1
        with open(PLIK, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Gap Sum = %d" % g, sum(w.values())] + [w.get(j, 0) for j in range(1, jmax + 1)])
        print("luka %d gotowa w %.2f h, zapisana do %s" % (g, (time.time() - t0) / 3600, PLIK), flush=True)
    print("Wszystkie luki gotowe -> %s" % PLIK)


print("Komorka C: G(%d#), luki %s, baza %d. Uruchom: licz()" % (HW.generuj_pierwsze(K)[-1], LUKI, BAZA))

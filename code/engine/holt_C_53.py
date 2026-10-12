# KOMORKA C - n_{g,j}(53#) dla nowych luk 106..116 (+ luki kontrolne 20, 30, 40).
# Wymaga komorki A (holt_A.py -> holt_worker.py). Zapis po kazdej luce do PLIK: przebieg mozna przerwac i wznowic.
# Kontrola: luki 20, 30, 40 musza sie zgadzac z nG47.csv przeniesionym o jeden krok jednolity (sprawdzi Claude).
import os, time, csv, multiprocessing, importlib
import holt_worker as HW
importlib.reload(HW)

K, BAZA = 16, 7                                   # G(53#), kolo bazowe 17#
LUKI = [20, 30, 40] + list(range(106, 117, 2))    # najpierw kontrolne (tanie), potem nowe
PLIK = "nG53_nowe.csv"
KAWALKI = 64


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
            if zrob % 16 == 0:
                print("     luka %d: %d/%d kawalkow, %.0f min" % (g, zrob, len(zad), (time.time() - t0) / 60), flush=True)
    return wyn


def licz_53(watki=None):
    gotowe = _gotowe()
    for g in LUKI:
        if g in gotowe:
            print("luka %d juz policzona" % g); continue
        t0 = time.time(); print("luka %d ..." % g, flush=True)
        w = _jedna_luka(g, watki)
        jmax = max(w) if w else 1
        with open(PLIK, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["Gap Sum = %d" % g, sum(w.values())] + [w.get(j, 0) for j in range(1, jmax + 1)])
        print("luka %d gotowa w %.1f h, zapisana do %s" % (g, (time.time() - t0) / 3600, PLIK), flush=True)
    print("Wszystkie luki gotowe -> %s" % PLIK)


print("Komorka C: G(53#), luki %s, baza %d. Uruchom: licz_53()" % (LUKI, BAZA))

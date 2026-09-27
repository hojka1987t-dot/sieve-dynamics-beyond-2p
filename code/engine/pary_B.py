import multiprocessing, time, csv, re, json, importlib
import pary_worker as PW
importlib.reload(PW)
if getattr(PW, "WERSJA", "0") < "5.0":
    raise ImportError("pary_worker.py to stara wersja albo uciety plik.")

def czytaj_csv(sciezka):
    d = {}
    with open(sciezka, encoding='utf-8-sig') as f:
        r = csv.reader(f); hdr = next(r)
        jcol = {int(re.search(r'\d+', h).group()): i for i, h in enumerate(hdr) if h.startswith('Length')}
        for row in r:
            m = re.search(r'Gap Sum = (\d+)', row[0])
            if m:
                d[int(m.group(1))] = {j: int(row[i]) for j, i in jcol.items()
                                      if i < len(row) and row[i].strip() not in ('', '0')}
    return d

def przejscie(k, r_base, gmin, gmax, plik_nastepny, watki=None, kawalki=32):
    """Struktura par w G(p_k#) dla g = gmin..gmax, dokladne przewidywanie G(q#)
    (q = nastepna liczba pierwsza) i porownanie z plikiem nastepnego etapu."""
    if watki is None: watki = multiprocessing.cpu_count()
    pr = PW.generuj_pierwsze(k + 1); q = pr[k]; Pb = 1
    for p in pr[:r_base]: Pb *= p
    print("PRZEJSCIE G(%d#) -> G(%d#), q=%d, 2q=%d, g=%d..%d" % (pr[k-1], q, q, 2*q, gmin, gmax))
    krok = max(1, Pb // kawalki)
    zad = [(k, r_base, g, q, a, min(a + krok, Pb + 1))
           for g in range(gmax, gmin - 1, -2) for a in range(1, Pb + 1, krok)]
    struk = {}; t0 = time.time(); zrob = 0
    with multiprocessing.Pool(watki) as pool:
        for g, w in pool.imap_unordered(PW.zadanie, zad):
            d = struk.setdefault(g, {})
            for key, c in w.items(): d[key] = d.get(key, 0) + c
            zrob += 1
            if zrob % max(1, len(zad) // 10) == 0:
                print("   %d/%d zadan, %.0f s" % (zrob, len(zad), time.time() - t0), flush=True)
    nast = czytaj_csv(plik_nastepny)
    print()
    print("    g   komorek zgodnych   podwojnych zlan (pary II)   najkrotszy czlon: teraz -> potem")
    ok = tot = 0
    for g in range(gmin, gmax + 1, 2):
        s = struk.get(g, {})
        pred = PW.przewiduj(s, q, g); fakt = nast.get(g, {})
        kl = set(pred) | set(fakt)
        zg = sum(1 for j in kl if pred.get(j, 0) == fakt.get(j, 0))
        ok += zg; tot += len(kl)
        ii = sum(c * key[2] for key, c in s.items())
        jm0 = min((key[0] for key, c in s.items() if c), default=None)
        jm1 = min((j for j, v in fakt.items() if v), default=None)
        print("  %4d      %3d/%-3d              %16d          %s -> %s"
              % (g, zg, len(kl), ii, jm0, jm1))
    print()
    print("  RAZEM zgodnych: %d/%d  -> %s" % (ok, tot, "MECHANIZM DOKLADNY" if ok == tot else "ROZBIEZNOSCI - sprawdzic"))
    with open("pary_G%d.json" % pr[k-1], "w") as f:
        json.dump({str(g): {"%d,%d,%d" % key: c for key, c in d.items()} for g, d in struk.items()}, f)
    print("  zapisano pary_G%d.json" % pr[k-1])
    return struk

print("Zaladowano. Kolejnosc (pliki CSV musza lezec w katalogu roboczym):")
print("  s37 = przejscie(12, 5, 80, 110, 'nG41_110.csv')   # ratunki 104 i 110")
print("  s41 = przejscie(13, 5, 84, 104, 'nG43_104.csv')")
print("  s43 = przejscie(14, 6, 92, 104, 'nG47.csv')")

import multiprocessing, time, csv, re, importlib
import holt_worker as HW
importlib.reload(HW)
if getattr(HW, "WERSJA", "0") < "4.1":
    raise ImportError("holt_worker.py to stara wersja albo uciety plik.")

def _licz(k, r_base, gmax, watki=None, kawalki=32):
    """n_{g,j}(p_k#) dla g = 2..gmax i wszystkich j. Zadania: (g, kawalek okien)."""
    if watki is None: watki = multiprocessing.cpu_count()
    pr = HW.generuj_pierwsze(k); Pb = 1
    for p in pr[:r_base]: Pb *= p
    krok = max(1, Pb // kawalki)
    zad = [(k, r_base, g, a, min(a + krok, Pb + 1))
           for g in range(gmax, 1, -2) for a in range(1, Pb + 1, krok)]
    wyn = {}; t0 = time.time(); zrob = 0
    with multiprocessing.Pool(watki) as pool:
        for g, w in pool.imap_unordered(HW.zadanie, zad):
            d = wyn.setdefault(g, {})
            for j, c in w.items(): d[j] = d.get(j, 0) + c
            zrob += 1
            if zrob % max(1, len(zad) // 10) == 0:
                print("   %d/%d zadan, %.0f s" % (zrob, len(zad), time.time() - t0), flush=True)
    print("   gotowe w %.0f s" % (time.time() - t0))
    return wyn

def waliduj_37(sciezka='nG37.csv', gmax=82, watki=None):
    """Porownanie z plikiem Holta: G(37#), wszystkie komorki n_{g,j} dla g<=gmax."""
    holt = {}
    with open(sciezka, encoding='utf-8-sig') as f:
        r = csv.reader(f); hdr = next(r)
        jcol = {int(re.search(r'\d+', h).group()): i for i, h in enumerate(hdr) if h.startswith('Length')}
        for row in r:
            m = re.search(r'Gap Sum = (\d+)', row[0])
            if not m: continue
            g = int(m.group(1))
            holt[g] = ({j: int(row[i]) for j, i in jcol.items() if i < len(row) and row[i].strip()},
                       int(row[1]))
    print("WALIDACJA G(37#) przeciw nG37.csv, g = 2..%d" % gmax)
    wyn = _licz(12, 5, gmax, watki)
    ok = bl = 0
    for g in range(2, gmax + 1, 2):
        h, tot = holt[g]; w = wyn.get(g, {})
        for j in set(h) | set(w):
            if h.get(j, 0) == w.get(j, 0): ok += 1
            else:
                bl += 1
                if bl <= 10: print("   ROZNICA g=%d j=%d: nasze %d, Holt %d" % (g, j, w.get(j, 0), h.get(j, 0)))
        if sum(w.values()) != tot:
            bl += 1; print("   ROZNICA sumy g=%d" % g)
    print("  zgodnych komorek: %d, roznic: %d  -> %s" % (ok, bl, "PELNA ZGODNOSC" if bl == 0 else "SPRAWDZIC"))
    return bl == 0

def warunki_poczatkowe(k, r_base, gmax, plik=None, watki=None):
    """n_{g,j}(p_k#) dla g<=gmax, zapis w formacie pliku Holta (Gap Sum, Totals, Length = j)."""
    pr = HW.generuj_pierwsze(k)
    if plik is None: plik = "nG%d.csv" % pr[k - 1]
    print("WARUNKI POCZATKOWE G(%d#), g = 2..%d, baza %d" % (pr[k - 1], gmax, r_base))
    wyn = _licz(k, r_base, gmax, watki)
    jmax = max((max(d) for d in wyn.values() if d), default=1)
    with open(plik, 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow([''] + ['Totals'] + ['Length = %d' % j for j in range(1, jmax + 1)])
        for g in range(2, gmax + 1, 2):
            d = wyn.get(g, {})
            wr.writerow(['Gap Sum = %d' % g, sum(d.values())] + [d.get(j, '') for j in range(1, jmax + 1)])
    print("  zapisano %s" % plik)
    return wyn

print("Zaladowano. Kolejnosc:")
print("  1) waliduj_37('nG37.csv', 82)          # musi dac PELNA ZGODNOSC")
print("  2) warunki_poczatkowe(13, 5, 84)        # G(41#): modele Holta do g<86")
print("  3) warunki_poczatkowe(14, 6, 92)        # G(43#): modele do g<94")

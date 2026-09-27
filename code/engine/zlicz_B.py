import multiprocessing
import time
import importlib
import zlicz_worker as Z

importlib.reload(Z)
if getattr(Z, "WERSJA", "0") < "3.1":
    raise ImportError("zlicz_worker.py na dysku to stara wersja albo uciety plik.")

# h(k) i n_seq z pliku remainders.txt Zillera - do kontroli
H = {6:22, 7:26, 8:34, 9:40, 10:46, 11:58, 12:66, 13:74, 14:90, 15:100,
     16:106, 17:118, 18:132, 19:152, 20:174}
NSEQ = {2:1, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:12, 10:2, 11:2, 12:24, 13:2,
        14:48, 15:24, 16:240, 17:60, 18:12, 19:144, 20:52}


def profil(k, r_base=None, Lmax=None, wezly_max=26, watki=None):
    """
    Pelny profil N_k(L) dla wszystkich parzystych L do Lmax.
    wezly_max: gorny limit wezlow w oknie - powyzej zliczanie staje sie
               niewykonalne (2^N stanow), wiec wartosc jest pomijana.
    """
    if r_base is None:
        r_base = max(3, k // 2 - 1)
    if Lmax is None:
        Lmax = H[k]
    if watki is None:
        watki = multiprocessing.cpu_count()
    print("=" * 62)
    print("PROFIL N_k(L) | k=%d  baza=%d  Lmax=%d  limit wezlow=%d  rdzeni=%d"
          % (k, r_base, Lmax, wezly_max, watki))
    print("=" * 62)
    t0 = time.time()
    zad = [(k, r_base, L, wezly_max) for L in range(2, Lmax + 1, 2)]
    wyn = {}
    with multiprocessing.Pool(watki) as pool:
        for r in pool.imap_unordered(Z.zadanie_L, zad):
            wyn[r['L']] = r
            if r['N'] is None:
                print("   L=%3d: pominiete (%d wezlow > limit)" % (r['L'], r['za_duzo']), flush=True)
            else:
                print("   L=%3d: N=%d   (okien %d)" % (r['L'], r['N'], r['okien']), flush=True)
    print()
    print("  czas: %.0f s" % (time.time() - t0))
    if k in NSEQ and H.get(k) in wyn and wyn[H[k]]['N'] is not None:
        a, b = wyn[H[k]]['N'], NSEQ[k]
        print("  KONTROLA: N_%d(h=%d) = %d, n_seq Zillera = %d  -> %s"
              % (k, H[k], a, b, "ZGODNE" if a == b else "ROZNICA - sprawdzic!"))
    return wyn


print("Zaladowano.")
print("  kontrola:  profil(12)   -> N_12(66) musi wyjsc 24")
print("  potem:     profil(14), profil(15), profil(16)")
print("  duze n_seq (rozstrzygajaca kontrola): profil(16) -> 240, profil(19) -> 144")

import multiprocessing, time, json, importlib
import klas_worker as KW
importlib.reload(KW)
if getattr(KW, "WERSJA", "0") < "6.0":
    raise ImportError("klas_worker.py to stara wersja albo uciety plik.")

# brakujace roznice Zillera od k+1 = 20 (wczesniej zabojstwa sa niemozliwe z twierdzenia)
# (k+1, g, etap k, baza) - bazy jak w weryfikatorze
PRZYPADKI = [
    (19, 146, 18, 7),                                   # KONTROLA: z twierdzenia musi wyjsc opoznienie
    (20, 166, 19, 7), (20, 170, 19, 7), (20, 172, 19, 7),
    (21, 182, 20, 7), (21, 186, 20, 7), (21, 188, 20, 7),
    (22, 194, 21, 7),
    (24, 230, 23, 8),
    (25, 254, 24, 8), (25, 256, 24, 8),
    (27, 278, 26, 9),
    (28, 296, 27, 9), (28, 298, 27, 9),
    (30, 328, 29, 10),
]

def sprawdz(k, r_base, g, a, watki=None, budzet=10**9):
    """Czy konstelacja (a, g-a) wystepuje w G(p_k#)? Wszystkie sektory, rownolegle."""
    if watki is None: watki = multiprocessing.cpu_count()
    top = KW.generuj_pierwsze(k)[r_base - 1]
    with multiprocessing.Manager() as mg:
        rozstrz = mg.dict()
        zad = [(k, r_base, g, a, budzet, c, rozstrz) for c in range(top)]
        ist = False; X = None; wer = None; przekr = False; okien = 0
        with multiprocessing.Pool(watki) as pool:
            for r in pool.imap_unordered(KW.zadanie_konst, zad):
                okien += r['okien']; przekr |= r['budzet_przekroczony']
                if r['istnieje'] and not ist:
                    ist = True; X = r['X']; wer = r['zweryfikowane']
    return ist, X, wer, przekr, okien

def klasyfikuj(przypadki=PRZYPADKI, watki=None, plik='klasyfikacja.json'):
    wyniki = []
    print("KLASYFIKATOR: brakujaca roznica g przy k+1 jest ZABOJSTWEM, jesli w G(p_k#)")
    print("wystepuje konstelacja (2q, g-2q), q = p_{k+1}; w przeciwnym razie OPOZNIENIEM.")
    print()
    for (k1, g, k, rb) in przypadki:
        q = KW.generuj_pierwsze(k1)[k1 - 1]; a = 2 * q
        t0 = time.time()
        ist, X, wer, przekr, okien = sprawdz(k, rb, g, a, watki)
        if ist and wer:
            werdykt = "ZABOJSTWO"
        elif ist and not wer:
            werdykt = "BLAD WERYFIKACJI - sprawdzic!"
        elif przekr:
            werdykt = "NIEPEWNE (budzet)"
        else:
            werdykt = "OPOZNIENIE"
        print("  k+1=%2d  g=%3d  (%d,%d) w G(%d#): %-11s  okien %d, %.0f s%s"
              % (k1, g, a, g - a, KW.generuj_pierwsze(k)[k - 1], werdykt, okien, time.time() - t0,
                 ("   swiadek X=%d" % X) if ist else ""), flush=True)
        wyniki.append({'k+1': k1, 'g': g, 'etap_k': k, 'baza': rb, 'a': a, 'werdykt': werdykt,
                       'X': X, 'zweryfikowane': wer, 'okien': okien, 'budzet': przekr})
        with open(plik, 'w') as f: json.dump(wyniki, f, indent=1)
    print()
    print("  zapisano", plik)
    return wyniki

print("Zaladowano. Uruchom:  w = klasyfikuj()")
print("Pierwszy wiersz (k+1=19, g=146) to kontrola - z twierdzenia MUSI wyjsc OPOZNIENIE.")

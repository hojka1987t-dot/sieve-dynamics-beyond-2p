import multiprocessing, time, json, importlib
import klas_worker as KW
importlib.reload(KW)
if getattr(KW, "WERSJA", "0") < "6.1":
    raise ImportError("klas_worker.py to stara wersja - uruchom najpierw komorke A.")

H = {19:152, 20:174, 21:190, 22:200, 23:216, 24:234, 25:258, 26:264, 27:282, 28:300, 29:312, 30:330}
BRAK = {20:[166,170,172], 21:[182,186,188], 22:[194], 23:[], 24:[230], 25:[254,256],
        26:[], 27:[278], 28:[296,298], 29:[], 30:[328]}
BAZA = {19:7, 20:7, 21:7, 22:8, 23:8, 24:8, 25:8, 26:9, 27:9, 28:9, 29:10}

def _rownolegle(fun, zad_bez_sektora, top, watki):
    with multiprocessing.Manager() as mg:
        rozstrz = mg.dict()
        zad = [z + (c, rozstrz) for c in range(top) for z in [zad_bez_sektora]]
        wynik = None; przekr = False; okien = 0
        with multiprocessing.Pool(watki) as pool:
            for r in pool.imap_unordered(fun, zad):
                okien += r['okien']; przekr |= r['budzet_przekroczony']
                if r['istnieje'] and wynik is None:
                    wynik = r
    return wynik, przekr, okien

def domknij(od=20, do=30, watki=None, budzet=10**9, plik='domkniecie.json'):
    """Dla kazdej OBECNEJ roznicy g z pasma (h(k), h(k+1)]: czy jest suma dwoch
    sasiednich luk w G(p_k#) nie zawierajacych luki 2q? Jesli nie - szuka ratunku
    przez trojke (u, 2q, w). Wszystko potwierdzane gcd-em."""
    if watki is None: watki = multiprocessing.cpu_count()
    wyniki = []; licz = {'PARA': 0, 'RATUNEK': 0, 'SPRZECZNOSC': 0, 'NIEPEWNE': 0}
    for k1 in range(od, do + 1):
        k = k1 - 1; rb = BAZA[k]
        q = KW.generuj_pierwsze(k1)[k1 - 1]; dq = 2 * q
        top = KW.generuj_pierwsze(k)[rb - 1]
        obecne = [g for g in range(H[k] + 2, H[k1] + 1, 2) if g not in BRAK[k1]]
        print("k+1=%d: pasmo (%d, %d], obecnych %d, etap G(%d#), 2q=%d"
              % (k1, H[k], H[k1], len(obecne), KW.generuj_pierwsze(k)[k - 1], dq), flush=True)
        for g in obecne:
            t0 = time.time()
            r, przekr, okien = _rownolegle(KW.zadanie_para,
                                           (k, rb, g, g - H[k], g // 2, (dq,), budzet), top, watki)
            if r and r['zweryfikowane']:
                t = r['wolne'][0]; typ = 'PARA'; opis = '(%d,%d)' % (t, g - t)
            else:
                typ = None; opis = ''
                for u in range(2, g - dq - 1, 2):
                    r2, p2, o2 = _rownolegle(KW.zadanie_wolne,
                                             (k, rb, g, (u, u + dq), budzet), top, watki)
                    przekr |= p2
                    if r2 and r2['zweryfikowane']:
                        r = r2; typ = 'RATUNEK'; opis = '(%d,%d,%d)' % (u, dq, g - dq - u); break
                if typ is None:
                    typ = 'NIEPEWNE' if przekr else 'SPRZECZNOSC'
            licz[typ] += 1
            print("    g=%3d: %-11s %-14s %6.0f s%s" % (g, typ, opis, time.time() - t0,
                  ("   X=%d" % r['X']) if r and r.get('istnieje') else ""), flush=True)
            wyniki.append({'k+1': k1, 'g': g, 'typ': typ, 'konstelacja': opis,
                           'X': r['X'] if r and r.get('istnieje') else None})
            with open(plik, 'w') as f: json.dump(wyniki, f, indent=1)
    print()
    print("PODSUMOWANIE:", licz)
    print("  PARA        - roznica urodzila sie jako suma dwoch sasiednich luk (prawo proste)")
    print("  RATUNEK     - urodzila sie WYLACZNIE przez trojke z luka 2q w srodku")
    print("  SPRZECZNOSC - nie znaleziono zadnej drogi narodzin (nie powinno sie zdarzyc)")
    return wyniki

print("Zaladowano. Uruchom:  w = domknij()")
print("Mozna tez po kawalku, np. domknij(20, 25), potem domknij(26, 30).")


# KOMORKA C - tylko wybrane roznice (uruchamiac PO komorkach A i B z domkniecia).
import time, multiprocessing

def domknij_wybrane(lista, watki=None, budzet=10**9):
    """lista: [(k+1, g), ...]. Dla kazdej: czy g jest suma dwoch sasiednich luk
    (bez luki 2q) w G(p_k#). Jesli NIE, a g wystepuje w tabeli Zillera,
    to urodzilo sie wylacznie z ratunku."""
    if watki is None: watki = multiprocessing.cpu_count()
    for k1, g in lista:
        k = k1 - 1; rb = BAZA[k]
        dq = 2 * KW.generuj_pierwsze(k1)[k1 - 1]
        top = KW.generuj_pierwsze(k)[rb - 1]
        t0 = time.time()
        r, przekr, okien = _rownolegle(KW.zadanie_para,
                                       (k, rb, g, g - H[k], g // 2, (dq,), budzet), top, watki)
        if r and r['zweryfikowane']:
            t = r['wolne'][0]
            print("k+1=%d  g=%d: PARA (%d,%d)   %.0f s   X=%d" % (k1, g, t, g - t, time.time() - t0, r['X']), flush=True)
        elif przekr:
            print("k+1=%d  g=%d: brak pary, ale BUDZET przekroczony - wynik niepewny   %.0f s" % (k1, g, time.time() - t0), flush=True)
        else:
            print("k+1=%d  g=%d: BRAK PARY (przeszukanie pelne) -> tylko ratunek   %.0f s" % (k1, g, time.time() - t0), flush=True)

print("Uruchom:  domknij_wybrane([(27, 280), (30, 326)])")
print("  PARA       -> brakujaca obok (278 / 328) to zwykla dziura")
print("  BRAK PARY  -> brakujaca obok lezy w cieniu ratunku, jak 186 i 188 przy k=21")

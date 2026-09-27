import multiprocessing
import time
import importlib
import roznice_worker as W

importlib.reload(W)
if getattr(W, "WERSJA", "0") < "2.0":
    raise ImportError("roznice_worker.py na dysku to stara wersja (nie strumieniowa).")

# Tabela Zillera (arXiv:2007.01808, tab. 1): k -> (h(k), [brakujace roznice])
ZILLER = {
    6:(22,[20]),   7:(26,[]),   8:(34,[32]),   9:(40,[]),  10:(46,[]),
    11:(58,[]),   12:(66,[]),  13:(74,[]),  14:(90,[86,88]), 15:(100,[98]),
    16:(106,[]),  17:(118,[]), 18:(132,[]), 19:(152,[146]),
    20:(174,[166,170,172]), 21:(190,[182,186,188]), 22:(200,[194]),
    23:(216,[]),  24:(234,[230]), 25:(258,[254,256]), 26:(264,[]),
    27:(282,[278]), 28:(300,[296,298]), 29:(312,[]), 30:(330,[328]),
    31:(354,[346,350,352]), 32:(378,[368,370,372,376]), 33:(388,[386]),
    34:(414,[406]), 35:(432,[424]), 36:(450,[446]), 37:(476,[468,472,474]),
    38:(492,[488]), 39:(510,[]), 40:(538,[530,536]), 41:(550,[]),
    42:(574,[572]), 43:(600,[592,596,598]), 44:(616,[]),
}


def sprawdz(k, r_base=None, Lmax=None, budzet_na_okno=10**8,
            liczba_watkow=None, porownaj=True):
    """
    Wersja STRUMIENIOWA: jednostka podzialu to sektor kola bazowego.
    Pamiec stala - nie powstaje tablica ocalalych, wiec baza 9 i 10 wchodza
    bez ograniczen pamieciowych.
    """
    if r_base is None:
        r_base = max(3, min(10, k // 2 - 1))
    if Lmax is None:
        if k not in ZILLER:
            raise ValueError("podaj Lmax - h(%d) nie jest w tabeli" % k)
        Lmax = ZILLER[k][0]
    if liczba_watkow is None:
        liczba_watkow = multiprocessing.cpu_count()

    primes = W.generuj_pierwsze(k)
    top = primes[r_base - 1]
    Ls = list(range(2, Lmax + 1, 2))

    print("=" * 66)
    print("WERYFIKACJA BRAKUJACYCH ROZNIC (strumien) | k=%d  baza=%d  Lmax=%d"
          % (k, r_base, Lmax))
    print("roznic: %d | sektorow: %d | zadan: %d | rdzeni: %d | budzet/okno: %d"
          % (len(Ls), top, len(Ls) * top, liczba_watkow, budzet_na_okno))
    print("=" * 66)

    t0 = time.time()
    okien = 0; krokow = 0
    swiadkowie = {}; przekr = set()

    mgr = multiprocessing.Manager()
    rozstrz = mgr.dict()
    # sektor na zewnatrz: kazda roznica dostaje najpierw sektor 0, potem 1, ...
    zad = [(k, r_base, L, budzet_na_okno, c, None, rozstrz)
           for c in range(top) for L in Ls]
    zrobione = 0
    with multiprocessing.Pool(processes=liczba_watkow) as pool:
        for w in pool.imap_unordered(W.zadanie_L, zad, chunksize=1):
            okien += w['okien']; krokow += w['krokow']
            zrobione += 1
            if w['budzet_przekroczony']: przekr.add(w['L'])
            if w['wystepuje'] and w['L'] not in swiadkowie:
                swiadkowie[w['L']] = w
            if zrobione % max(1, len(zad) // 8) == 0:
                print("     %d/%d zadan, otwartych roznic: %d, %.0f s"
                      % (zrobione, len(zad), len(Ls) - len(rozstrz), time.time() - t0))
    t = time.time() - t0

    brak = sorted(L for L in Ls if L not in swiadkowie)
    zle_zweryf = [L for L, w in swiadkowie.items() if not w['zweryfikowane']]
    grozne = sorted(set(przekr) & set(brak))
    niegrozne = sorted(set(przekr) - set(brak))

    print()
    print("--- CERTYFIKAT ---")
    print("  przeszukano wszystkie %d sektorow z ogonem przez granice: TAK" % top)
    print("  okien sprawdzonych: %d | krokow dfs: %d" % (okien, krokow))
    if grozne:
        print("  !!! BUDZET WYCZERPANY dla BRAKUJACYCH L=%s" % grozne)
        print("  !!! Dla tych L wynik NIE jest dowodem. Podnies budzet_na_okno.")
    else:
        print("  budzet nie wiazal dla zadnej brakujacej roznicy -> kazde 'brak' jest DOWODEM")
    if niegrozne:
        print("  (budzet wyczerpany dla L=%s, ale te maja swiadka - bez wplywu)" % niegrozne)
    if zle_zweryf:
        print("  !!! swiadek nie przeszedl weryfikacji gcd dla L=%s - BLAD" % zle_zweryf)
    else:
        print("  kazdy znaleziony swiadek zweryfikowany niezaleznie przez gcd: TAK")
    print()
    print("--- WYNIK ---")
    print("  brakujace roznice <= %d: %s" % (Lmax, brak))
    if porownaj and k in ZILLER:
        z = ZILLER[k][1]
        print("  tabela Zillera:          %s" % z)
        print("  >>> %s" % ("ZGODNE" if brak == z else "ROZNICA - sprawdzic trzykrotnie!"))
    print()
    print("  czas: %.1f s" % t)
    return brak, swiadkowie


print("Zaladowano (strumien). Wywolanie w osobnej komorce, np.:  sprawdz(23, r_base=8)")

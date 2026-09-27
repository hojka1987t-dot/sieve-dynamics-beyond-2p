import multiprocessing, time, importlib
import ratunek_worker as RW
importlib.reload(RW)
H = {19:152, 20:174, 21:190, 22:200, 23:216, 24:234, 25:258, 26:264, 27:282, 28:300, 29:312, 30:330}
BAZA = {19:7, 20:7, 21:7, 22:8, 23:8, 24:8, 25:8, 26:9, 27:9, 28:9, 29:10}

def sprawdz_ratunek(k1, g, watki=None, budzet=10**10):
    """Czy g NA PEWNO nie jest suma dwoch sasiednich luk (bez luki 2q) w G(p_k#)?"""
    if watki is None: watki = multiprocessing.cpu_count()
    k = k1 - 1; rb = BAZA[k]
    dq = 2 * RW.generuj_pierwsze(k1)[k1 - 1]
    top = RW.generuj_pierwsze(k)[rb - 1]
    t0 = time.time()
    with multiprocessing.Manager() as mg:
        rozstrz = mg.dict()
        zad = [(k, rb, g, g - H[k], g // 2, (dq,), budzet, c, rozstrz) for c in range(top)]
        znal = None; przekr = []; okien = 0; csp = 0
        with multiprocessing.Pool(watki) as pool:
            for r in pool.imap_unordered(RW.zadanie_para_r, zad):
                przekr += r['przekroczone']; okien += r['okien']; csp += r['csp']
                if r['istnieje'] and znal is None: znal = r
    print("k+1=%d g=%d:" % (k1, g))
    if znal:
        print("   PARA ISTNIEJE: (%d,%d), X=%d, zweryfikowane=%s  -> to NIE byl ratunek (artefakt budzetu)"
              % (znal['para'][0], znal['para'][1], znal['X'], znal['zweryfikowane']))
    elif przekr:
        print("   brak pary, ale %d zadan przekroczylo budzet - wynik NIEPEWNY" % len(przekr))
    else:
        print("   BRAK PARY - przeszukanie pelne: %d okien, %d zadan CSP, 0 przekroczen budzetu"
              % (okien, csp))
        print("   -> jesli ta roznica WYSTEPUJE w tabeli Zillera, to urodzila sie wylacznie")
        print("      przez podwojne zlanie: RATUNEK POTWIERDZONY")
    print("   czas %.0f s" % (time.time() - t0))
    return znal, przekr

print("Zaladowano. Uruchom dla kazdego ratunku:  sprawdz_ratunek(k+1, g)")

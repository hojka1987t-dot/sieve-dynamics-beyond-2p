# KOMORKA T - porownanie workerow 4.1 i 4.5 okno po oknie: przy 53# (arytmetyka int64) i przy 73#, 79#
# (iloczyn klas > 2^63, czyli sciezka wielomodularna). Wymaga holt_A_41.py i holt_A_45.py obok.
import random, time, importlib
from math import gcd, prod
for wersja in ("41", "45"):
    src = open("holt_A_%s.py" % wersja, encoding="utf-8").read()
    kod = src.split("kod = r'''", 1)[1].split("'''", 1)[0]
    open("holt_worker_%s.py" % wersja, "w", encoding="utf-8").write(kod)
import holt_worker_41 as A, holt_worker_45 as E
importlib.reload(A); importlib.reload(E)
random.seed(1)
for K, BAZA, g, ile in [(16, 7, 60, 20), (16, 7, 80, 8), (16, 6, 106, 2), (21, 5, 50, 6), (22, 4, 40, 6)]:
    pr = A.generuj_pierwsze(K); Pb = prod(pr[:BAZA]); fale = pr[BAZA:K]
    zgodne = n = 0; ta = te = 0.0
    while n < ile:
        v0 = random.randrange(1, Pb)
        if gcd(v0, Pb) != 1 or gcd(v0 + g, Pb) != 1: continue
        wez = [i for i in range(1, g) if gcd(v0 + i, Pb) == 1]
        t0 = time.time(); ra = A.rozklad_csp(wez, fale, g); ta += time.time() - t0
        t0 = time.time(); re = E.rozklad_csp(wez, fale, g, blok=10); te += time.time() - t0
        zgodne += (ra == re); n += 1
    print("%d#, kolo %d#, g=%d: %d/%d okien zgodnych; czas okna 4.1: %.3f s, 4.5: %.4f s"
          % (pr[-1], pr[BAZA - 1], g, zgodne, n, ta / n, te / n), flush=True)

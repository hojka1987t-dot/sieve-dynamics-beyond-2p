# KOMORKA T - porownanie workerow 4.1 i 4.5 okno po oknie: przy 53# (arytmetyka int64) i przy 73#, 79#
# (iloczyn klas > 2^63, czyli sciezka wielomodularna).
# Zrodla workerow: 4.5 - holt_A_45.py (ten folder); 4.1 - holt_A_41.py, jesli lezy obok,
# a w przeciwnym razie code/engine/holt_A.py z repozytorium (to ta sama komorka A wersji 4.1).
import os, random, time, importlib
from math import gcd, prod

ZRODLA = {"41": ["holt_A_41.py", os.path.join("..", "engine", "holt_A.py")],
          "45": ["holt_A_45.py"]}


def _zrodlo(wersja):
    for sciezka in ZRODLA[wersja]:
        if os.path.exists(sciezka):
            return sciezka
    raise FileNotFoundError("brak komorki A wersji %s: szukano %s" % (wersja, ZRODLA[wersja]))


for wersja in ("41", "45"):
    with open(_zrodlo(wersja), encoding="utf-8") as f:
        src = f.read()
    kod = src.split("kod = r'''", 1)[1].split("'''", 1)[0]
    with open("holt_worker_%s.py" % wersja, "w", encoding="utf-8") as f:
        f.write(kod)
importlib.invalidate_caches()
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

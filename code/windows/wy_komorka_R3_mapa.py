# Komorka R3 - MAPA GLEBOKOSCI przez lancuch rekurencji warstwowej (na noc). Wymaga komorki R1 (wy_rek_worker.py).
# Baza startowa liczona wprost; potem kolejne liczby pierwsze rekurencja z certyfikatem.
# Dla kazdej dlugosci y zapisuje: W, glebokosc (najmniejsze j z W+j-C_j = minimum), C_0..C_J, certyfikat.
import os, time, importlib
from multiprocessing import Pool
import wy_rek_worker as RW
importlib.reload(RW)

BAZA_START = [2, 3, 5, 7, 11, 13]          # 13#, liczona wprost
ETAPY = [17, 19, 23, 29, 31, 37]           # kolejne q
Y_OD, Y_DO, KROK = 700, 1500, 4
LIMIT_S = 1800
PLIK = "mapa_glebokosci.txt"


def _W_wprost(pr, ys):
    N = 1
    for p in pr: N *= p
    ym = max(ys); M = N + ym + 2
    ocal = [1] * M
    for p in pr:
        for v in range(0, M, p): ocal[v] = 0
    pre = [0]
    for v in ocal: pre.append(pre[-1] + v)
    return {y: min(pre[x + y + 1] - pre[x] for x in range(N)) for y in ys}


def mapa(ys=None):
    ys = ys or list(range(Y_OD, Y_DO + 1, KROK))
    gotowe = {}
    if os.path.exists(PLIK):
        for l in open(PLIK):
            if l.strip() and not l.startswith("#"):
                c = l.split(); gotowe[(int(c[0]), int(c[1]))] = int(c[2])
    t0 = time.time()
    W = _W_wprost(BAZA_START, ys); z0 = BAZA_START[-1]
    print("baza startowa %d#: W policzone wprost (%.0f s)" % (z0, time.time() - t0), flush=True)
    with open(PLIK, "a") as f:
        if not gotowe:
            f.write("# q y W_nowe glebokosc certyfikat C_0..C_J czas_s\n")
        for q in ETAPY:
            nowe = {y: gotowe[(q, y)] for y in ys if (q, y) in gotowe}
            zadania = [(z0, q, y, W[y], LIMIT_S) for y in ys if y not in nowe]
            t1 = time.time()
            with Pool() as pool:
                for y, w, J, cert, C, t in pool.imap_unordered(RW._W_nastepne, zadania):
                    gl = min(j for j in range(len(C)) if W[y] + j - C[j] == w) if (cert and w is not None) else -1
                    f.write("%d %d %s %d %s %s %.1f\n" % (q, y, w, gl, "TAK" if cert else "NIE", ",".join(map(str, C)), t))
                    f.flush(); nowe[y] = w
            print("etap q=%d gotowy: %d dlugosci w %.1f min" % (q, len(zadania), (time.time() - t1) / 60), flush=True)
            if any(nowe[y] is None for y in ys):
                print("!!! etap q=%d ma wyniki bez certyfikatu - lancuch zatrzymany" % q); return
            W = nowe; z0 = q
    print("Mapa gotowa (%.1f h) -> %s" % ((time.time() - t0) / 3600, PLIK))


print("Komorka R3: mapa glebokosci, start %d#, etapy q = %s, y = %d..%d co %d. Uruchom: mapa()"
      % (BAZA_START[-1], ETAPY, Y_OD, Y_DO, KROK))

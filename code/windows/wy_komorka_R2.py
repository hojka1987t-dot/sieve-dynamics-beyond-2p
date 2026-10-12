# Komorka R2 - REKURENCJA WARSTWOWA (sterowanie). Wymaga wczesniejszego uruchomienia komorki R1.
# W_{qN}(y) = min_j (W + j - C_j); certyfikat pojemnosci daje wynik DOKLADNY, niezaleznie od prawa "+1".
import os, time, importlib
from multiprocessing import Pool
import wy_rek_worker as RW
importlib.reload(RW)

Z_STARE, Q_NOWE = 73, 79
Y_OD, Y_DO = 198, 700
LIMIT_S = 900
PLIK_WYJ = "profil_rek_z%d.txt" % Q_NOWE


def rekurencja(z0=Z_STARE, q=Q_NOWE, y_od=Y_OD, y_do=Y_DO, plik=None):
    plik = plik or PLIK_WYJ
    W = RW._wczytaj(z0)
    zrobione = set()
    if os.path.exists(plik):
        for l in open(plik):
            if l.strip() and not l.startswith("#"):
                zrobione.add(int(l.split()[0]))
    zadania = [(z0, q, y, W[y], LIMIT_S) for y in range(y_od, y_do + 1, 2) if y in W and y not in zrobione]
    t0 = time.time(); n = 0
    with Pool() as pool, open(plik, "a") as f:
        if not zrobione:
            f.write("# y W_nowe J certyfikat C_0..C_J czas_s\n")
        for y, w, J, cert, C, t in pool.imap_unordered(RW._W_nastepne, zadania):
            f.write("%d %s %d %s %s %.1f\n" % (y, w, J, "TAK" if cert else "NIE", ",".join(map(str, C)), t))
            f.flush(); n += 1
            if n % 25 == 0:
                print("  rekurencja: %d/%d dlugosci, %.0f s" % (n, len(zadania), time.time() - t0), flush=True)
    print("Gotowe: %d dlugosci w %.1f min -> %s" % (n, (time.time() - t0) / 60, plik))


print("Komorka R2: rekurencja %d -> %d dla y=%d..%d. Uruchom: rekurencja()" % (Z_STARE, Q_NOWE, Y_OD, Y_DO))

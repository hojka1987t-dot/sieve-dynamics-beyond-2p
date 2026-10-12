%%writefile wy_rek_worker.py
"""Funkcje robocze rekurencji warstwowej dla W (phi_min) - modul importowany przez procesy robocze."""
import time
# Pojemnosc klasy: S(n) = najwieksza liczba ocalalych wsrod n kolejnych wyrazow ciagu o kroku 2q.
# Dokladnie dla n <= 17; dalej bezpieczne ograniczenie S(a+b) <= S(a) + S(b) (zawsze poprawne).
_S = [0, 1, 2, 2, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 9, 10]
_U = list(_S)


def _S_gorne(n):
    while len(_U) <= n:
        m = len(_U)
        _U.append(min(_S[a] + _U[m - a] for a in range(1, 18)))
    return _U[n]


def _pojemnosc(y, q):
    return _S_gorne(y // (2 * q) + 1)


def _pierwsze_do(z):
    return [p for p in range(2, z + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


def _szukaj(z0, q, y, cnt, cel, limit_s):
    """Czy istnieje okno [0,y] bazy z0 z dokladnie cnt ocalalymi i klasa mod q >= cel?"""
    P = _pierwsze_do(z0); n = y + 1
    maski = [[sum(1 << v for v in range(a, n, p)) for a in range(p)] for p in P]
    qm = [sum(1 << v for v in range(b, n, q)) for b in range(q)]
    t0 = time.time(); licz = [0]; wynik = [False]

    def dfs(i, niep):
        if wynik[0]:
            return
        licz[0] += 1
        if licz[0] % 100000 == 0 and time.time() - t0 > limit_s:
            raise TimeoutError
        if max((niep & m).bit_count() for m in qm) < cel:
            return
        u = niep.bit_count()
        if i == len(P):
            if u == cnt:
                wynik[0] = True
            return
        moga = 0
        for k in range(i, len(P)):
            moga += max((niep & m).bit_count() for m in maski[k])
        if u - moga > cnt:
            return
        for a in sorted(range(P[i]), key=lambda a: -(niep & maski[i][a]).bit_count()):
            dfs(i + 1, niep & ~maski[i][a])
            if wynik[0]:
                return
    try:
        dfs(0, (1 << n) - 1)
        return "TAK" if wynik[0] else "NIE"
    except TimeoutError:
        return "LIMIT"


def _C_max(z0, q, y, cnt, cmax, limit_s):
    for c in range(cmax, 0, -1):
        st = _szukaj(z0, q, y, cnt, c, limit_s)
        if st == "TAK":
            return c
        if st == "LIMIT":
            return None
    return 0


def _W_nastepne(args):
    z0, q, y, W, limit_s = args
    t0 = time.time()
    if W == 0:
        return y, 0, 0, True, [], 0.0
    cy = _pojemnosc(y, q)
    najl = None; C = []; j = 0
    while True:
        c = _C_max(z0, q, y, W + j, cy, limit_s)
        if c is None:
            return y, najl, j, False, C, time.time() - t0
        C.append(c)
        v = W + j - c
        najl = v if najl is None else min(najl, v)
        if W + j + 1 - cy >= najl:          # certyfikat: wiecej ocalalych nie pomoze
            return y, najl, j, True, C, time.time() - t0
        j += 1


def _dane(nazwa, *podfoldery):
    """Plik danych: najpierw w biezacym folderze, potem w data/ archiwum (uruchamianie z code/<folder>)."""
    import os
    for p in (nazwa, os.path.join('..', '..', 'data', *podfoldery, nazwa)):
        if os.path.exists(p):
            return p
    return nazwa


def _wczytaj(z):
    d = {}
    for l in open(_dane("profil_z%d.txt" % z, "windows", "profiles")):
        if l.strip():
            y, w, _ = l.split(); d[int(y)] = int(w)
    return d

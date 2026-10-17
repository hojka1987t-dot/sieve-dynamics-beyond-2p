"""Pelna weryfikacja danych konstelacji (pary, trojki, czworki; etapy 5#..47#; rozpietosc <= 104):
1) suma po dlugosciach = iloczyn CRT dla kazdej konstelacji; 2) suma po wszystkich konstelacjach z m lukami o rozpietosci g
   = C(J-1, m-1) n_{g,J} dla luk z tego samego etapu (odbicie dodawane z ta sama populacja); 3) rekurencja jednolita
   n'_J = (q-J-1) n_J + (J+1-m) n_{J+1} miedzy kolejnymi, niezaleznie liczonymi etapami tam, gdzie rozpietosc < 2q."""
from math import prod, comb
from _wspolne import ETAPY, PR, konstelacje, luki, punkty

def krok(w, q, m):
    n = {}
    for J in range(m, (max(w) if w else 0) + 1):
        v = (q - J - 1) * w.get(J, 0) + (J + 1 - m) * w.get(J + 1, 0)
        if v: n[J] = v
    return n

def sprawdz(m):
    bl_crt = bl_sum = bl_rek = n_rek = 0; poprz = None
    for p in ETAPY:
        K = konstelacje(m, p); G = luki(p); P = [q for q in PR if q <= p]
        for s, w in K.items():
            if sum(w.values()) != prod(q - len({c % q for c in punkty(s)}) for q in P): bl_crt += 1
        pelne = {}
        for s, w in K.items(): pelne[s] = w; pelne[s[::-1]] = w
        for (g,), wg in G.items():
            if g > 104: continue
            suma = {}
            for s, w in pelne.items():
                if sum(s) == g:
                    for J, c in w.items(): suma[J] = suma.get(J, 0) + c
            if suma != {J: comb(J - 1, m - 1) * c for J, c in wg.items() if J >= m}: bl_sum += 1
        if poprz:
            for s, w in poprz.items():
                if sum(s) < 2 * p:
                    n_rek += 1; bl_rek += krok(w, p, m) != K.get(s, {})
        poprz = K
    print('m = %d: konstelacji %d; bledow CRT %d; sum wobec luk %d; rekurencja: %d sprawdzen, bledow %d'
          % (m, len(K), bl_crt, bl_sum, n_rek, bl_rek), flush=True)

if __name__ == '__main__':
    for m in (2, 3, 4): sprawdz(m)

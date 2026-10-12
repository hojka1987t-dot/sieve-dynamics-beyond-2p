"""Sprawdzenie dowodu koniecznosci w Tw. 5.1: dla kazdej konstelacji s, dla ktorej istnieje zaludniony ksztalt
z dwoma punktami przystajacymi mod q, niech J* = najwieksza dlugosc takiego ksztaltu. Wtedy
n_{s,J*}(qN) - [(q-J*-1) n_{s,J*}(N) + (J*+1-m) n_{s,J*+1}(N)] = sum_{P przystajace, dl. J*} m_P (|P| - nu_q(P)) > 0."""
import sys
from collections import defaultdict
from weryfikacja_wyczerpujaca import ksztalty, punkty, klasy

def test(primes, q, S):
    _, mN = ksztalty(primes, S); _, mQ = ksztalty(primes + [q], S)
    nN = defaultdict(lambda: defaultdict(int)); nQ = defaultdict(lambda: defaultdict(int))
    nadw = defaultdict(lambda: defaultdict(int))       # C -> J -> sum m_P (|P| - nu_q(P)) po ksztaltach przystajacych
    for mapa, cel, zrodlo in ((mN, nN, True), (mQ, nQ, False)):
        for P, c in mapa.items():
            pts = punkty(P); L = pts[-1]; wew = pts[1:-1]; J = len(pts) - 1
            d = len(pts) - len(klasy(pts, q)) if zrodlo else 0
            for r in range(1 << len(wew)):
                C = (0,) + tuple(wew[i] for i in range(len(wew)) if r >> i & 1) + (L,)
                cel[C][J] += c
                if d: nadw[C][J] += c * d
    zgodne = zle = 0
    for C, dj in nadw.items():
        m = len(C) - 1; Js = max(dj)
        rzecz = nQ[C].get(Js, 0) - ((q - Js - 1) * nN[C].get(Js, 0) + (Js + 1 - m) * nN[C].get(Js + 1, 0))
        if rzecz == dj[Js] and rzecz > 0: zgodne += 1
        else: zle += 1
    print(f'N={"*".join(map(str,primes))} -> q={q}: konstelacji z przystającym kształtem: {len(nadw)}; '
          f'nadwyżka przy J* zgodna z wzorem i dodatnia: {zgodne}, niezgodna: {zle}')

if __name__ == "__main__":
  for pr, q in (([2,3,5,7],11), ([2,3,5,7,11],13), ([2,3,5,7,11,13],17), ([2,3,5,7,11,13,17],19), ([2,3,7,11,13],5), ([2,3,5,11,13],7)):
      test(pr, q, 40)

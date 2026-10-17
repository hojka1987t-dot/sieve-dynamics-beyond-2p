"""Dokladne modele Holta dla par i trojek kolejnych luk od p0 = 47 (kazdy krok od 53 jest jednolity dla rozpietosci <= 104).
Konstelacja z m lukami: L_j = sum_{i>=j} C(i-m, j-m) n_{s,i}(47#), D_m = prod_{m+1 < p <= 47}(p-m-1), l_k = L_{m+k-1}/D_m,
w_s(p#) = sum_k (-1)^(k-1) l_k prod_{47<q<=p}(q-m-k)/(q-m-1); dla m = 1 to dokladnie konwencja Dodatku A pracy.
Kontrole: l_1 = prod_{p<=m+1}(p-nu_p) * prod_{p>m+1}(p-nu_p)/(p-m-1) (iloraz Hardy'ego-Littlewooda) dla kazdej konstelacji;
dla m = 1 kod odtwarza opublikowane wspolczynniki luk (data/wspolczynniki_l.csv) co do ulamka.
Wynik: data/constellations/model_coefficients_p0_47.csv."""
import os, csv
from fractions import Fraction
from math import prod, comb
from _wspolne import ROOT, DATA, PR, konstelacje, luki, punkty
P = [p for p in PR if p <= 47]

def wspolczynniki(m, w):
    D = prod(p - m - 1 for p in P if p > m + 1); Jmax = max(w); out = {}
    for j in range(m, Jmax + 1):
        L = sum(comb(i - m, j - m) * w.get(i, 0) for i in range(j, Jmax + 1))
        if L: out[j - m + 1] = Fraction(L, D)
    return out

def hl(s):
    C = punkty(s); m = len(s)
    return prod(Fraction(p - len({c % p for c in C})) for p in P if p <= m + 1) * \
           prod(Fraction(p - len({c % p for c in C}), p - m - 1) for p in P if p > m + 1)

if __name__ == '__main__':
    G = luki(47); pub = {}
    for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'wspolczynniki_l.csv'), encoding='utf-8')):
        if int(r['p0']) == 47: pub.setdefault(int(r['g']), {})[int(r['j'])] = Fraction(r['l_j_dokladnie'])
    wsp = [g for g in pub if (g,) in G]
    print('m = 1: zgodnosc z opublikowanymi wspolczynnikami luk:', all(wspolczynniki(1, G[(g,)]) == pub[g] for g in wsp), '(%d luk)' % len(wsp))
    wiersze = []; zle = 0; ile = 0
    for m in (2, 3):
        for s, w in sorted(konstelacje(m, 47).items(), key=lambda t: (sum(t[0]), t[0])):
            l = wspolczynniki(m, w); ile += 1; zle += l.get(1) != hl(s)
            for k, v in sorted(l.items()):
                wiersze.append([','.join(map(str, s)), m, 47, k, '%d/%d' % (v.numerator, v.denominator), '%.15g' % float(v)])
    print('l_1 = iloraz Hardy\'ego-Littlewooda: %d konstelacji, niezgodnych %d' % (ile, zle))
    with open(os.path.join(DATA, 'model_coefficients_p0_47.csv'), 'w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f); wr.writerow(['constellation', 'm', 'p0', 'k', 'l_k_exact', 'l_k_decimal']); wr.writerows(wiersze)
    print('zapisano %d wspolczynnikow' % len(wiersze))

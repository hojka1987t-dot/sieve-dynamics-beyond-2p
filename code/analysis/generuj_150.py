"""Generator dla wersji 3: dokladne wspolczynniki l_j modeli Holta dla wszystkich parzystych g <= 150.
Zrodla (kazde sprawdzone osobno: suma CRT, momenty k <= 4, luki kontrolne):
  g <= 104: nG47.csv (p0 = 47); 106-112: nG53_106_112.csv (metoda 1, = metoda 2); 114-116: nG53_45.csv;
  118-120: nG59_45.csv; 122-132: nG61_45.csv; 134-140: nG67_45.csv; 142-144: nG71_45.csv; 146-150: nG73_45.csv.
Wynik: wspolczynniki_l.csv (dokladne ulamki), tabela1_wiersze.tex, dodatekA_wiersze.tex."""
import csv, os, sys
from fractions import Fraction
from math import comb, prod
KAT = sys.argv[1] if len(sys.argv) > 1 else '.'
ZRODLA = [(47, 'nG47.csv', range(2, 105, 2)), (53, 'nG53_106_112.csv', range(106, 113, 2)), (53, 'nG53_45.csv', (114, 116)),
          (59, 'nG59_45.csv', (118, 120)), (61, 'nG61_45.csv', range(122, 133, 2)), (67, 'nG67_45.csv', range(134, 141, 2)),
          (71, 'nG71_45.csv', (142, 144)), (73, 'nG73_45.csv', (146, 148, 150))]
def wczytaj(p):
    d = {}
    with open(p, encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0].startswith('Gap Sum'):
                d[int(r[0].split('=')[1])] = [int(x) if x.strip() else 0 for x in r[2:]]
    return d
def D(p0): return prod(p - 2 for p in range(3, p0 + 1) if all(p % d for d in range(2, int(p ** .5) + 1)))
wsp = {}; brak = []
for p0, plik, luki in ZRODLA:
    sciezka = os.path.join(KAT, plik)
    dane = wczytaj(sciezka) if os.path.exists(sciezka) else {}
    for g in luki:
        if g not in dane: brak.append((g, plik)); continue
        w = [Fraction(v, D(p0)) for v in dane[g]]
        while w and w[-1] == 0: w.pop()
        wsp[g] = (p0, [sum(comb(i, j) * w[i] for i in range(j, len(w))) for j in range(len(w))])
if brak:
    print('BRAKUJE luk (nie generuje plikow):', brak); sys.exit(1)
# kontrola l_1 = S(g)/S(2) dla kazdej luki
for g, (p0, l) in wsp.items():
    oczek = prod(Fraction(q - 1, q - 2) for q in range(3, g + 1) if g % q == 0 and all(q % d for d in range(2, int(q ** .5) + 1)))
    assert l[0] == oczek, ('l_1', g)
with open('wspolczynniki_l.csv', 'w', encoding='utf-8') as f:
    f.write('g,p0,j,l_j_dokladnie,l_j_dziesietnie\n')
    for g in sorted(wsp):
        p0, l = wsp[g]
        for j, x in enumerate(l, 1): f.write('%d,%d,%d,%d/%d,%.15g\n' % (g, p0, j, x.numerator, x.denominator, float(x)))
with open('tabela1_wiersze.tex', 'w', encoding='utf-8') as f:
    for g in range(84, 151, 2):
        p0, l = wsp[g]; f.write('%d & %d & %.6f & %.4f & %.4f \\\\\n' % (g, p0, float(l[0]), float(l[1]), float(l[2])))
with open('dodatekA_wiersze.tex', 'w', encoding='utf-8') as f:
    p_pop = None
    for g in sorted(wsp):
        p0, l = wsp[g]
        if p0 != p_pop:
            f.write('\\multicolumn{2}{l}{$p_0 = %d$} \\\\\n' % p0); p_pop = p0
        f.write('%d & %s \\\\\n' % (g, ', '.join('%.8g' % float(x) for x in l)))
print('luk:', len(wsp), '| wspolczynnikow:', sum(len(l) for _, l in wsp.values()), '| l_1 = S(g)/S(2) dla wszystkich: TAK')

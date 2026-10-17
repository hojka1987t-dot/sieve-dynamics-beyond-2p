"""Tabela brakujacych konstelacji (definicje jak dla tabeli Zillera w pracy, rozdz. 6.3): przy etapie q# konstelacja s
o m lukach brakuje, gdy jej rozpietosc jest mniejsza niz zasieg (najwieksza rozpietosc obecnej konstelacji z m lukami,
w granicach <= 104), a n_{s,m}(q#) = 0. Brak dziedziczony: ktoras luka s nie wystepuje; z polaczenia: kazda wystepuje.
Przyczyna: opoznienie, gdy n_{s,m+1}(N) = 0 przy poprzednim etapie N; zablokowane narodziny, gdy n_{s,m+1}(N) > 0
(wtedy kazdy driving term z jednym dodatkowym punktem ma ten punkt w klasie punktu konstelacji mod q).
Wynik: data/constellations/missing_constellations.txt."""
import os
from _wspolne import DATA, ETAPY, konstelacje, luki

def tabela(m):
    linie = ['m = %d' % m, 'etap  obecnych  zasieg  brakow  dziedziczonych  z_polaczenia  opoznien  zablokowanych  zablokowane (n_{s,m+1}(N))']
    poprz = konstelacje(m, ETAPY[0])
    for i, p in enumerate(ETAPY[1:], 1):
        K = konstelacje(m, p); G = luki(p)
        jest = lambda s: K[s].get(m, 0) > 0
        ob = [s for s in K if jest(s)]; R = max(sum(s) for s in ob) if ob else 0
        brak = [s for s in K if sum(s) < R and not jest(s)]
        dz = [s for s in brak if any(G.get((d,), {}).get(1, 0) == 0 for d in s)]
        pol = [s for s in brak if s not in dz]
        zab = [s for s in pol if poprz[s].get(m + 1, 0) > 0]
        linie.append('%3d#  %8d  %6d  %6d  %14d  %12d  %8d  %13d  %s' % (p, len(ob), R, len(brak), len(dz), len(pol), len(pol) - len(zab), len(zab),
                     ' '.join('%s(%d)' % (','.join(map(str, s)), poprz[s][m + 1]) for s in sorted(zab, key=lambda t: (sum(t), t)))))
        poprz = K
    return linie

if __name__ == '__main__':
    tekst = '\n'.join(sum((tabela(m) + [''] for m in (2, 3, 4)), []))
    print(tekst)
    open(os.path.join(DATA, 'missing_constellations.txt'), 'w', encoding='utf-8').write(tekst)

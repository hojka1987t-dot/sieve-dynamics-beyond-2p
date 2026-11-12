"""Akapit o najwiekszych lukach w przedzialach przetrwania (rozdzial 6.4 wersji 3, pytanie Holta z [Ho26b, par. 4.1]).

Dla kazdego przedzialu [p_k^2, p_{k+1}^2) do 10^9 (ostatni przedzial uciety na 10^9) liczy najwieksza luke miedzy
kolejnymi liczbami pierwszymi na dwa sposoby i porownuje ja z progiem 2p_k + 4 (hipoteza Legendre'a):
  - luka LEZACA w przedziale: oba konce w [p_k^2, p_{k+1}^2),
  - luka ZACZYNAJACA SIE w przedziale: poczatek w [p_k^2, p_{k+1}^2), koniec moze byc dalej (tak liczy sito.py, 'maxg').
Wlasne sito segmentowe, bez innych plikow. Wynik w wersji 3: 0.515 przy p_k = 31 (luka lezaca, powyzej polowy progu
tylko tam, 3401 przedzialow od p_k = 2); 0.778 przy p_k = 7 (luka 113 -> 127 zaczynajaca sie w przedziale);
przy p_k = 311 (k = 64) najwieksza luka 42.
Uruchomienie: python prog_legendre.py   (ok. minuty, ok. 1 GB pamieci; mniejsze SEG zmniejsza pamiec)."""
import numpy as np, time

LIM = 10**9
SEG = 10**8

t0 = time.time()
mal = np.ones(31623 + 1, bool); mal[:2] = False
for i in range(2, 178):
    if mal[i]: mal[i * i::i] = False
P = np.nonzero(mal)[0].astype(np.int64)      # p_k do 31623; p_k^2 < 10^9 dla p_k <= 31607
kw = P * P                                    # poczatki przedzialow przetrwania
K = len(P)
max_lez = np.zeros(K, np.int64)               # najwieksza luka lezaca w przedziale k
max_start = np.zeros(K, np.int64)             # najwieksza luka zaczynajaca sie w przedziale k
gdzie_lez = np.zeros(K, np.int64)             # poczatek takiej luki
gdzie_start = np.zeros(K, np.int64)
ost = None
for lo in range(0, LIM, SEG):
    hi = min(lo + SEG, LIM); s = np.ones(hi - lo, bool)
    if lo == 0: s[:2] = False
    for p in P:
        if p * p >= hi: break
        st = max(p * p, ((lo + p - 1) // p) * p); s[st - lo::p] = False
    pr = np.nonzero(s)[0].astype(np.int64) + lo
    if ost is not None: pr = np.concatenate(([ost], pr))
    a = pr[:-1]; b = pr[1:]; g = b - a; ost = int(pr[-1])
    ka = np.searchsorted(kw, a, side='right') - 1     # przedzial poczatku
    kb = np.searchsorted(kw, b, side='right') - 1     # przedzial konca
    for maks, gdzie, sel in ((max_start, gdzie_start, ka >= 0), (max_lez, gdzie_lez, (ka >= 0) & (ka == kb))):
        kk = ka[sel]; gg = g[sel]; aa = a[sel]
        if len(kk) == 0: continue
        # najwieksza luka w kazdym przedziale tego segmentu (przy rownych - pierwsza)
        kol = np.lexsort((aa, -gg, kk))
        kk, gg, aa = kk[kol], gg[kol], aa[kol]
        pierwsze = np.r_[True, kk[1:] != kk[:-1]]
        kk, gg, aa = kk[pierwsze], gg[pierwsze], aa[pierwsze]
        lepsze = gg > maks[kk]
        maks[kk[lepsze]] = gg[lepsze]; gdzie[kk[lepsze]] = aa[lepsze]

prog = 2 * P + 4
ile = int((kw < LIM).sum())                    # przedzialy z poczatkiem ponizej 10^9
print('sito do 10^9: %.0f s; przedzialow przetrwania od p_k = 2: %d, od p_k = 47: %d'
      % (time.time() - t0, ile, ile - int(np.nonzero(P == 47)[0][0])))
print()
for nazwa, maks, gdzie in (('lezaca w przedziale', max_lez, gdzie_lez), ('zaczynajaca sie w przedziale', max_start, gdzie_start)):
    r = maks[:ile] / prog[:ile]
    i = int(np.argmax(r))
    nad = np.nonzero(r > 0.5)[0]
    print('luka %s:' % nazwa)
    print('   najwiekszy stosunek do 2p_k + 4: %.4f przy p_k = %d (luka %d od %d do %d, prog %d)'
          % (r[i], P[i], maks[i], gdzie[i], gdzie[i] + maks[i], prog[i]))
    print('   powyzej polowy progu w %d z %d przedzialow: %s'
          % (len(nad), ile, ', '.join('p_k = %d (%.4f)' % (P[j], r[j]) for j in nad)))
    j311 = int(np.nonzero(P == 311)[0][0])
    print('   p_k = 311 (k = %d): najwieksza luka %d (od %d); najwieksza dla k <= 64: %d'
          % (j311 + 1, maks[j311], gdzie[j311], int(maks[:64].max())))
    print()

# KOMORKA: celowane wyszukiwanie swiadkow-PAR dla 5 roznic (wymaga para_worker.py i roznice_worker.py w folderze notatnika)
import json, time, multiprocessing as mp
import para_worker as PW, roznice_worker as W
from math import gcd, prod

CELE = {23: [202, 206, 210], 24: [224, 226]}

def szukaj_par(cele=CELE, r_base=7, budzet=10**8):
    wyniki = {}
    for k, Ls in cele.items():
        P = W.generuj_pierwsze(k); top = P[r_base - 1]
        for L in Ls:
            t0 = time.time(); znal = None; budz = 0; sekt = 0
            with mp.Pool() as pool:
                for r in pool.imap_unordered(PW.para_sektor, [(k, L, r_base, s, budzet) for s in range(top)]):
                    sekt += 1; budz += r['budzet_przekroczony']
                    if r['V'] is not None:
                        znal = r; pool.terminate(); break
            if znal:
                V = znal['V']
                ok = [x for x in range(L + 1) if gcd(V + x, prod(P)) == 1] == [0, L]
                wew = [x for x in range(1, L) if gcd(V + x, prod(P[:-1])) == 1]
                wpis = {'status': 'PARA' if ok and len(wew) == 1 else 'BLAD WERYFIKACJI', 'V': str(V), 'wnetrze_na_etapie_k-1': wew}
            elif budz:
                wpis = {'status': 'NIEROZSTRZYGNIETE (budzet przekroczony w %d sektorach)' % budz}
            else:
                wpis = {'status': 'BRAK PARY (przeszukano wszystkie %d sektory, budzet nie wiazal)' % sekt}
            wpis['czas_s'] = round(time.time() - t0)
            wyniki['%d,%d' % (k, L)] = wpis
            print(k, L, wpis['status'], wpis.get('wnetrze_na_etapie_k-1', ''), '| %d s' % wpis['czas_s'], flush=True)
            with open('pary_wyniki.json', 'w', encoding='utf-8') as f:
                json.dump(wyniki, f, indent=1)
    return wyniki

szukaj_par()

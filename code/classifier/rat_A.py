# KOMORKA A - zapis workera sprawdzajacego ratunki (osobny plik, nie rusza klas_worker.py).
kod = r'''# Sprawdzenie ratunkow: pelne przeszukanie par z budzetem NA KAZDE wywolanie CSP.
from klas_worker import generuj_pierwsze, solve_csp_z, BudzetWyczerpany, _okna, _swiadek
WERSJA = "1.0"

def zadanie_para_r(args):
    k, r_base, g, t_min, t_max, wyklucz, budzet, sektor, rozstrz = args
    if rozstrz is not None and 'znal' in rozstrz:
        return {'istnieje': False, 'przekroczone': [], 'okien': 0, 'csp': 0, 'pominiete': True}
    fale = generuj_pierwsze(k)[r_base:k]
    przekr = []; okien = 0; csp = 0
    for v0, wez in _okna(k, r_base, g, sektor):
        kand = [t for t in wez if t_min <= t <= t_max and t not in wyklucz and (g - t) not in wyklucz]
        if not kand: continue
        okien += 1
        for t in kand:
            wz = [w for w in wez if w != t]
            licznik = [0]; csp += 1                     # budzet na TO jedno zadanie
            try:
                ok, asg = solve_csp_z(wz, fale, (0, t, g), budzet, licznik)
            except BudzetWyczerpany:
                przekr.append((v0, t)); continue
            if ok:
                if rozstrz is not None: rozstrz['znal'] = True
                X, wer = _swiadek(k, r_base, g, (t,), v0, asg)
                return {'istnieje': True, 'X': X, 'zweryfikowane': wer, 'para': (t, g - t),
                        'przekroczone': przekr, 'okien': okien, 'csp': csp, 'pominiete': False}
    return {'istnieje': False, 'przekroczone': przekr, 'okien': okien, 'csp': csp, 'pominiete': False}
'''
with open('ratunek_worker.py', 'w', encoding='utf-8') as f:
    f.write(kod)
import os
print('zapisano', os.path.getsize('ratunek_worker.py'), 'bajtow')

import time, importlib
import sat_model as S
importlib.reload(S)

# (opis, etap k, g, punkty wolne, oczekiwany wynik)
KONTROLE = [
    ("kontrola: para (58,116), k+1=20",           19, 174, (58,),      'SAT'),
    ("kontrola: ratunek (10,146,34), k+1=21",     20, 190, (10, 156),  'SAT'),
    ("kontrola: luka 134 > h(18), nie moze byc",  18, 146, (134,),     'UNSAT'),
]
# brakujace roznice: czy istnieje konstelacja (2q, g-2q)? Klasyfikator: NIE (opoznienie)
ZABOJSTWA = [(20,166),(20,170),(20,172),(21,182),(21,186),(21,188),(22,194),
             (24,230),(25,254),(25,256),(27,278),(28,296),(28,298),(30,328)]

def uruchom(limit_s=3600, watki=16, solver='cpsat'):
    print("NIEZALEZNE SPRAWDZENIE solverem %s (limit %d s na przypadek)" % (solver, limit_s))
    przypadki = list(KONTROLE)
    for k1, g in ZABOJSTWA:
        q = S.pierwsze(k1)[-1]
        przypadki.append(("k+1=%d g=%d: czy (%d,%d) wystepuje?" % (k1, g, 2*q, g - 2*q), k1 - 1, g, (2*q,), 'UNSAT'))
    zgodne = 0
    for opis, k, g, wolne, oczek in przypadki:
        t0 = time.time()
        m = S.buduj_model(k, g, wolne)
        if solver == 'cpsat':
            wyn, wyb = S.rozwiaz_cpsat(m, limit_s, watki)
        else:
            wyb = S.rozwiaz_przeglad(m); wyn = 'SAT' if wyb else 'UNSAT'
        uwaga = ''
        if wyn == 'SAT':
            x = S.swiadek(m[0], wyb)
            uwaga = 'swiadek gcd: %s' % ('OK' if S.sprawdz_swiadka(x, g, wolne, m[0]) else 'ZLY!')
        ok = (wyn == oczek)
        zgodne += ok
        print("  %-46s %-17s oczek. %-5s %s  %6.0f s  %s" % (opis, wyn, oczek, 'OK ' if ok else '<<<', time.time() - t0, uwaga), flush=True)
    print()
    print("  zgodnych z oczekiwaniem: %d z %d" % (zgodne, len(przypadki)))
    print("  UNSAT dla brakujacej roznicy = solver DOWODZI, ze to nie zabojstwo, tylko opoznienie")

print("Uruchom:  uruchom()      (NIEROZSTRZYGNIETE = limit czasu; wtedy mozna zwiekszyc limit_s)")

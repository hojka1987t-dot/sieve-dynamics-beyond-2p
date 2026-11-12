"""Walidacja modelu SAT (sat_model.py) wobec sily: 70 losowych konstelacji w G(19#) (rozdzial 7 wersji 3).

Dla kazdej konstelacji (1-3 kolejne luki, kazda parzysta 2..36, rozpietosc <= 72):
  - sila: przeglad calego cyklu G(19#) - czy konstelacja gdzies wystepuje (numpy),
  - model: buduj_model + rozwiaz_przeglad (wyczerpujacy przeglad, bez OR-Tools); jesli SAT, swiadek x z chinskiego
    twierdzenia o resztach jest sprawdzany gcd-em i musi byc jednym z polozen znalezionych przez sile,
  - jesli jest zainstalowany OR-Tools: takze rozwiaz_cpsat.
Oczekiwane: wszystkie 70 zgodne (30 konstelacji wystepuje, 40 nie). Uruchomienie z tego folderu:
python walidacja_brute.py   (kilkanascie sekund, ok. 0,5 GB pamieci).
Jesli brak sat_model.py, jest on tworzony z komorki sat_A.py."""
import os, random, time
from math import prod
import numpy as np

if not os.path.exists('sat_model.py'):                      # tresc modelu z komorki A
    with open('sat_A.py', encoding='utf-8') as f:
        kod = f.read().split("kod = r'''", 1)[1].split("'''", 1)[0]
    with open('sat_model.py', 'w', encoding='utf-8') as f:
        f.write(kod)
import sat_model as S

K = 8                       # G(19#)
ILE, SEED = 70, 5
P = S.pierwsze(K); N = prod(P)
ROZP = 72

x = np.arange(N + ROZP + 1, dtype=np.int64)
wzg = np.ones(x.size, bool)
for p in P: wzg &= (x % p != 0)                             # wzg[t]: t wzglednie pierwsze z 19#
cs = np.concatenate(([0], np.cumsum(wzg, dtype=np.int64)))  # cs[t] = liczba wzgl. pierwszych < t
idx = np.arange(N)

def sila(luki):
    """Wszystkie x mod 19#, przy ktorych w G(19#) zaczyna sie konstelacja o tych lukach."""
    C = [0]
    for d in luki: C.append(C[-1] + d)
    g = C[-1]; maska = np.ones(N, bool)
    for c in C: maska &= wzg[c:c + N]
    wewn = cs[idx + g] - cs[idx + 1]                         # liczba wzgl. pierwszych w (x, x + g)
    return C, set(np.nonzero(maska & (wewn == len(C) - 2))[0].tolist())

try:
    import ortools  # noqa: F401
    CPSAT = True
except ImportError:
    CPSAT = False

random.seed(SEED)
konst = []
while len(konst) < ILE:
    m = random.choice((1, 2, 3))
    luki = tuple(2 * random.randint(1, 18) for _ in range(m))
    if sum(luki) <= ROZP and luki not in konst:
        konst.append(luki)

t0 = time.time(); zgodne = sat = 0
for luki in konst:
    C, polozenia = sila(luki)
    model = S.buduj_model(K, C[-1], C[1:-1])
    wyb = S.rozwiaz_przeglad(model)
    ok = (wyb is not None) == bool(polozenia)
    uwaga = ''
    if wyb is not None:
        xs = S.swiadek(model[0], wyb)
        ok &= S.sprawdz_swiadka(xs, C[-1], C[1:-1], model[0]) and xs in polozenia
        uwaga = 'swiadek %d' % xs
    if CPSAT:
        wyn, _ = S.rozwiaz_cpsat(model, 60, 1)
        ok &= (wyn == 'SAT') == bool(polozenia)
        uwaga += '  CP-SAT %s' % wyn
    zgodne += ok; sat += bool(polozenia)
    print('  %-14s sila: %6d wystapien   model: %-5s %s  %s'
          % (','.join(map(str, luki)), len(polozenia), 'SAT' if wyb is not None else 'UNSAT', 'OK ' if ok else '<<<', uwaga))
print()
print('zgodnych: %d z %d (wystepuje: %d, nie wystepuje: %d)%s;  %.0f s'
      % (zgodne, len(konst), sat, len(konst) - sat, '' if CPSAT else '; OR-Tools niezainstalowany - CP-SAT pominiety',
         time.time() - t0))

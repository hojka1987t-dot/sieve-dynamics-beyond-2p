# Niezalezne sprawdzenie: czy konstelacja wystepuje w G(p_k#) - jako zadanie spelnialnosci.
# Zadnych okien, kola bazowego ani kodu silnika. Punkty 0, wolne i g nie moga byc pokryte;
# kazdy inny punkt przedzialu musi byc pokryty przez klase reszt jakiejs liczby pierwszej.
from math import gcd, prod

def pierwsze(n):
    p = []; x = 2
    while len(p) < n:
        if all(x % d for d in p if d * d <= x): p.append(x)
        x += 1
    return p

def buduj_model(k, g, wolne):
    """Klasy c_p (przesuniecia pokrywane przez p) i dla kazdego punktu - czym moze byc pokryty."""
    P = pierwsze(k)
    niepokr = {0, g} | set(wolne)
    dozw = {p: [c for c in range(p) if all(t % p != c for t in niepokr)] for p in P}
    pokr = []
    for t in range(1, g):
        if t in niepokr: continue
        opcje = [(p, t % p) for p in P if (t % p) in dozw[p]]
        pokr.append((t, opcje))
    return P, dozw, pokr

def swiadek(P, wybor):
    """x z wyboru klas: x = -c_p (mod p)."""
    M = prod(P); x = 0
    for p in P:
        Mi = M // p
        x += (-wybor[p] % p) * Mi * pow(Mi, -1, p)
    return x % M

def sprawdz_swiadka(x, g, wolne, P):
    M = prod(P); zb = {0, g} | set(wolne)
    return all((gcd(x + t, M) == 1) == (t in zb) for t in range(g + 1))

def rozwiaz_przeglad(model):
    """Prosty, wyczerpujacy przeglad - tylko do walidacji modelu na malych k."""
    P, dozw, pokr = model
    if any(not dozw[p] for p in P) or any(not o for _, o in pokr): return None
    wybor = {}
    def rek(i):
        # wybierz niepokryty punkt z najmniejsza liczba opcji
        best = None
        for t, opcje in pokr:
            if any(wybor.get(p) == c for p, c in opcje): continue
            wolne_op = [(p, c) for p, c in opcje if p not in wybor]
            if not wolne_op: return None
            if best is None or len(wolne_op) < len(best): best = wolne_op
        if best is None:
            return dict(wybor)
        for p, c in best:
            wybor[p] = c
            r = rek(i + 1)
            if r: return r
            del wybor[p]
        return None
    r = rek(0)
    if r is None: return None
    for p in P:
        if p not in r: r[p] = dozw[p][0]
    return r

def rozwiaz_cpsat(model, limit_s=600, watki=8):
    """To samo zadanie gotowym solverem CP-SAT (Google OR-Tools)."""
    from ortools.sat.python import cp_model
    P, dozw, pokr = model
    if any(not dozw[p] for p in P) or any(not o for _, o in pokr): return 'UNSAT', None
    m = cp_model.CpModel(); y = {}
    for p in P:
        v = [m.NewBoolVar('y_%d_%d' % (p, c)) for c in dozw[p]]
        for c, b in zip(dozw[p], v): y[(p, c)] = b
        m.AddExactlyOne(v)
    for t, opcje in pokr:
        m.AddBoolOr([y[o] for o in opcje])
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = limit_s
    s.parameters.num_workers = watki
    st = s.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return 'SAT', {p: next(c for c in dozw[p] if s.Value(y[(p, c)])) for p in P}
    if st == cp_model.INFEASIBLE:
        return 'UNSAT', None
    return 'NIEROZSTRZYGNIETE', None

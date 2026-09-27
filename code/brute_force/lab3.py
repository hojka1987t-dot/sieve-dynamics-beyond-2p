import numpy as np, random, time
from math import prod
from lab import cykl

def jmin_do(gaps, Gmax):
    """Dla kazdej rozpietosci g <= Gmax: najkrotszy czlon (liczba luk) w cyklu."""
    n = len(gaps); S = np.concatenate(([0], np.cumsum(np.concatenate((gaps, gaps, gaps)))))
    jm = {}
    idx = np.arange(n)
    for k in range(1, 2 * n):
        sp = S[idx + k] - S[idx]
        ok = sp <= Gmax
        if not ok.any(): break
        for g in np.unique(sp[ok]).tolist():
            if g not in jm: jm[g] = k
    return jm

def porownaj(S, s0):
    G = [cykl(S[:s + 1]) for s in range(len(S))]
    D = [set(np.unique(g).tolist()) for g in G]
    h = [max(d) for d in D]
    jm = jmin_do(G[s0], h[-1] + 40)
    lin_D = {s: {g for g, j in jm.items() if j <= s - s0 + 1} for s in range(s0, len(S))}
    lin_h = {s: max(lin_D[s]) for s in lin_D}
    trw_lin = []; trw_real = []; bl_lin = 0; bl_real = 0
    for s in range(s0 + 1, len(S)):
        bl_lin += sum(1 for g in range(2, lin_h[s], 2) if g not in lin_D[s])
        bl_real += sum(1 for g in range(2, h[s], 2) if g not in D[s])
        if s >= s0 + 2:
            trw_lin += [(s, g) for g in range(2, lin_h[s - 1] + 1, 2) if g not in lin_D[s]]
        trw_real += [(s, g) for g in range(2, h[s - 1] + 1, 2) if g not in D[s]]
    return trw_lin, trw_real, bl_lin, bl_real

if __name__ == "__main__":
    random.seed(5); POOL = [3,5,7,11,13,17,19,23,29,31]
    t0 = time.time(); ile = 0; TL = 0; TR = 0; BL = 0; BR = 0; sita_z_tl = []
    while time.time() - t0 < 230:
        k = random.randint(6, 8); S = [2] + random.sample(POOL, k)
        if prod(S) > 2 * 10**7: continue
        for s0 in (1, 2):
            tl, tr, bl, br = porownaj(S, s0)
            ile += 1; TL += len(tl); TR += len(tr); BL += bl; BR += br
            if tl: sita_z_tl.append((S, s0, tl[:3]))
    print("porownan (sito x etap startowy): %d" % ile)
    print("brakujacych roznic:   model liniowy %d,   prawdziwe sito %d" % (BL, BR))
    print("TRWALYCH dziur:       model liniowy %d,   prawdziwe sito %d" % (TL, TR))
    print("porownan, w ktorych model liniowy ma trwala dziure: %d" % len(sita_z_tl))
    for x in sita_z_tl[:6]: print("   ", x)

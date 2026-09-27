import numpy as np, random, time
from math import prod
from lab import cykl

POOL = [3,5,7,11,13,17,19,23,29,31,37,41,43]

def analiza(S):
    """Dla kazdej brakujacej roznicy: pary (a,b), ktore rodza ja w nastepnym kroku."""
    uzyte = set(S); qx = next(p for p in POOL if p not in uzyte)
    G = [cykl(S[:s + 1]) for s in range(len(S))]
    D = [set(np.unique(g).tolist()) for g in G]
    h = [max(d) for d in D]
    rek = []
    for s in range(1, len(S)):
        q = S[s + 1] if s + 1 < len(S) else qx
        gaps = G[s]; nxt = np.roll(gaps, -1)
        m = (gaps % (2 * q) == 0); mn = np.roll(m, -1)
        sumy = gaps + nxt
        for g in range(2, h[s], 2):
            if g in D[s]: continue
            sel = (sumy == g) & ~m & ~mn
            pary = sorted(set(zip(gaps[sel].tolist(), nxt[sel].tolist())))
            wszystkie = sorted(set(zip(gaps[sumy == g].tolist(), nxt[sumy == g].tolist())))
            rek.append({'S': S, 's': s, 'g': g, 'h_prev': h[s - 1], 'h': h[s],
                        'pary': pary, 'pary_wsz': wszystkie, 'q': q})
    return rek

if __name__ == "__main__":
    random.seed(11); t0 = time.time(); R = []; ile = 0
    while time.time() - t0 < 200:
        k = random.randint(5, 8); S = [2] + random.sample(POOL[:11], k)
        if prod(S) > 3 * 10**7: continue
        R += analiza(S); ile += 1
    print("sit: %d, brakujacych roznic: %d" % (ile, len(R)))
    print()
    ur_para = [r for r in R if r['pary']]
    print("urodzone w nastepnym kroku z kwalifikujacej sie PARY: %d z %d" % (len(ur_para), len(R)))
    bez = [r for r in R if not r['pary']]
    print("bez kwalifikujacej sie pary: %d" % len(bez))
    for r in bez[:5]: print("   ", r['S'], 'etap', r['s'], 'g', r['g'], 'pary (wszystkie):', r['pary_wsz'][:4])
    print()
    # ksztalt: mniejsza luka w najlepszej parze
    mins = [min(min(a, b) for a, b in r['pary']) for r in ur_para]
    from collections import Counter
    c = Counter(mins)
    print("najmniejsza luka w parze rodzacej (min po parach):", sorted(c.items())[:10])
    # czy wieksza luka pary jest 'nowa' (wieksza od h poprzedniego etapu)?
    nowa = sum(1 for r in ur_para if any(max(a, b) > r['h_prev'] for a, b in r['pary']))
    print("pary, w ktorych wieksza luka jest NOWA (> poprzednie maksimum): %d z %d" % (nowa, len(ur_para)))
    tylko_nowe = sum(1 for r in ur_para if all(max(a, b) > r['h_prev'] for a, b in r['pary']))
    print("roznice, dla ktorych KAZDA rodzaca para ma nowa luke: %d z %d" % (tylko_nowe, len(ur_para)))

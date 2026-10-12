import sys, time
import numpy as np
from collections import Counter

def pierwsze(n):
    p = []; x = 2
    while len(p) < n:
        if all(x % d for d in p if d * d <= x): p.append(x)
        x += 1
    return p

def analiza(r, ys, partia=20000):
    pr = pierwsze(r + 1); q = pr[r]; P = 1
    for p in pr[:r]: P *= p
    L = P + max(ys) + 1
    s = np.ones(L, dtype=np.int8)
    for p in pr[:r]: s[::p] = 0
    cs = np.concatenate(([0], np.cumsum(s, dtype=np.int32)))
    rq = (np.arange(L) % q).astype(np.int32)
    wyn = []
    for y in ys:
        n = cs[y + 1: y + 1 + P] - cs[:P]
        Wmin = int(n.min()); cmax = y // (2 * q) + 1
        J = 2
        while True:
          X = np.nonzero(n <= Wmin + J)[0]
          C = {}; best_v = None; jopt = set(); off = np.arange(y + 1)
          for b0 in range(0, X.size, partia):
              B = X[b0:b0 + partia]; idx = B[:, None] + off[None, :]
              sv = s[idx].astype(bool); rows = np.broadcast_to(np.arange(B.size)[:, None], idx.shape)
              cnt = np.bincount(rows[sv] * q + rq[idx][sv], minlength=B.size * q).reshape(B.size, q)
              c = cnt.max(axis=1); nv = n[B]; j = nv - Wmin; v = nv - c
              for jj in np.unique(j):
                  C[int(jj)] = max(C.get(int(jj), -1), int(c[j == jj].max()))
              mv = int(v.min())
              if best_v is None or mv < best_v: best_v = mv; jopt = set()
              if mv == best_v: jopt |= set(int(t) for t in np.unique(j[v == mv]))
          kompletne = (Wmin + J + 1 - cmax) > best_v
          if kompletne or J >= cmax: break
          J += 1
        wyn.append((y, Wmin, best_v, sorted(jopt), C, kompletne, X.size))
    return q, wyn

def zapisz(wyn, q, r):
    with open('szt_wyniki_r%d.txt' % r, 'a') as f:
        for y, W, Wn, jo, C, k, nk in wyn:
            f.write('%d %d %d %s %s %d %d\n' % (y, W, Wn, ','.join(map(str, jo)), ','.join('%d:%d' % (j, c) for j, c in sorted(C.items())), int(k), nk))

if __name__ == '__main__':
    r, y0, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time(); q, wyn = analiza(r, list(range(y0, y1 + 1, 2))); zapisz(wyn, q, r)
    zl = [w for w in wyn if max(w[3]) > 1]
    szt = []
    for y, W, Wn, jo, C, k, nk in wyn:
        for j, c in C.items():
            if j >= 2 and 0 in C and c - C[0] > j - 1: szt.append((y, j, c - C[0])); break
    print('baza %d -> %d (q=%d): y=%d..%d (%d dlugosci), czas %.0f s, okien sprawdzonych lacznie %d'
          % (r, r + 1, q, y0, y1, len(wyn), time.time() - t0, sum(w[6] for w in wyn)))
    print('  kompletnosc dla wszystkich y:', all(w[5] for w in wyn))
    print('  PRAWO (kazde optimum bazy r+1 ma przodka gorszego o <= 1): %d/%d' % (len(wyn) - len(zl), len(wyn)))
    if zl: print('    zlamania (y, j przodkow optimow):', [(w[0], w[3]) for w in zl[:10]])
    print('  SZTYWNOSC KLAS (C_j - C_0 <= j-1 dla j>=2): %d/%d' % (len(wyn) - len(szt), len(wyn)))
    if szt: print('    naruszenia (y, j, przyrost):', szt[:10])
    for j in (1, 2, 3, 4):
        print('    przyrost C_%d - C_0:' % j, dict(sorted(Counter(w[4][j] - w[4][0] for w in wyn if j in w[4] and 0 in w[4]).items())))

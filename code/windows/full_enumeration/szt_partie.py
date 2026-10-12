"""Pelne wyliczenie okien dla duzego kola (partiami pozycji). Uzycie: python szt_partie.py r y0 y1 [krok] [J]"""
import sys, time
import numpy as np

def pierwsze(n):
    p = []; x = 2
    while len(p) < n:
        if all(x % d for d in p if d * d <= x): p.append(x)
        x += 1
    return p

def analiza(r, ys, J=3, C=8_000_000, partia=20000):
    pr = pierwsze(r + 1); q = pr[r]; P = 1
    for p in pr[:r]: P *= p
    ymax = max(ys)
    Wmin = {y: None for y in ys}; pary = {y: [] for y in ys}      # pary (n, c) dla okien n <= Wmin+J
    for x0 in range(0, P, C):
        dl = min(C, P - x0); L = dl + ymax + 1
        s = np.ones(L, dtype=np.int8)
        for p in pr[:r]: s[(-x0) % p::p] = 0
        cs = np.concatenate(([0], np.cumsum(s, dtype=np.int32)))
        rq = ((x0 + np.arange(L, dtype=np.int64)) % q).astype(np.int32)
        for y in ys:
            n = cs[y + 1: y + 1 + dl] - cs[:dl]
            m = int(n.min())
            if Wmin[y] is None or m < Wmin[y]:
                Wmin[y] = m; pary[y] = [t for t in pary[y] if t[0] <= m + J]
            X = np.nonzero(n <= Wmin[y] + J)[0]
            off = np.arange(y + 1)
            for b0 in range(0, X.size, partia):
                B = X[b0:b0 + partia]; idx = B[:, None] + off[None, :]
                sv = s[idx].astype(bool); rows = np.broadcast_to(np.arange(B.size)[:, None], idx.shape)
                cnt = np.bincount(rows[sv] * q + rq[idx][sv], minlength=B.size * q).reshape(B.size, q)
                c = cnt.max(axis=1); nv = n[B]
                pary[y].extend(zip(nv.tolist(), c.tolist()))
    wyn = []
    for y in ys:
        W = Wmin[y]; cmax = y // (2 * q) + 1
        C_ = {}; best = None; jopt = set()
        for nv, c in pary[y]:
            if nv > W + J: continue
            j = nv - W; C_[j] = max(C_.get(j, -1), c); v = nv - c
            if best is None or v < best: best = v; jopt = {j}
            elif v == best: jopt.add(j)
        komp = (W + J + 1 - cmax) > best
        wyn.append((y, W, best, sorted(jopt), C_, komp))
    return q, wyn

if __name__ == '__main__':
    r, y0, y1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    krok = int(sys.argv[4]) if len(sys.argv) > 4 else 2; J = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    t0 = time.time(); q, wyn = analiza(r, list(range(y0, y1 + 1, krok)), J=J)
    with open('szt_wyniki_r%d.txt' % r, 'a') as f:
        for y, W, Wn, jo, C_, k in wyn:
            f.write('%d %d %d %s %s %d\n' % (y, W, Wn, ','.join(map(str, jo)), ','.join('%d:%d' % (j, c) for j, c in sorted(C_.items())), int(k)))
    print('baza %d -> %d (q=%d): %d dlugosci y=%d..%d, J=%d, czas %.0f s, kompletnych %d'
          % (r, r + 1, q, len(wyn), y0, y1, J, time.time() - t0, sum(1 for w in wyn if w[5])))

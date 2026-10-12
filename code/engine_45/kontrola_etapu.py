import csv, sys, time
from itertools import combinations
from math import comb
def _dane(nazwa, *podfoldery):
    """Plik danych: najpierw w biezacym folderze, potem w data/ archiwum (uruchamianie z code/<folder>)."""
    import os
    for p in (nazwa, os.path.join('..', '..', 'data', *podfoldery, nazwa)):
        if os.path.exists(p):
            return p
    return nazwa


def wczytaj(p):
    d={}
    with open(p,encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0].startswith('Gap Sum'):
                g=int(r[0].split('=')[1]); v=[int(x) if x.strip() else 0 for x in r[2:]]
                tot=int(r[1]) if r[1].strip() else None
                while v and v[-1]==0: v.pop()
                d[g]=(tot,v)
    return d
def pierwsze_do(z): return [p for p in range(2,z+1) if all(p%d for d in range(2,int(p**.5)+1))]
def moment(g,k,P):
    pos=list(range(2,g,2)); rk={p:[t%p for t in pos] for p in P}; S=0
    for T in combinations(range(len(pos)),k):
        f=1
        for p in P:
            kl={0,g%p}
            for i in T: kl.add(rk[p][i])
            f*=p-len(kl)
            if f==0: break
        S+=f
    return S
def kontrola(plik, pz, kmax=4):
    P=pierwsze_do(pz); dane=wczytaj(plik); n47=wczytaj(_dane('nG47.csv'))
    print(f'=== {plik} (G({pz}#)): luki {sorted(dane)}')
    kroki=[p for p in P if p>47]
    for g in (20,40,60):
        if g not in dane: print(f'   luka kontrolna {g}: BRAK W PLIKU'); continue
        w=n47[g][1][:]
        for q in kroki:                                   # kroki jednolite 47 -> pz (g <= 60 < 2q)
            a=w+[0,0]; w=[(q-J-1)*a[J-1]+J*a[J] for J in range(1,len(w)+1)]
            while w and w[-1]==0: w.pop()
        print(f'   luka kontrolna {g}: {"ZGODNA co do jednostki" if w==dane[g][1] else "ROZNA !!!"}')
    for g in sorted(dane):
        if g<=60: continue
        tot,v=dane[g]; oczek=1
        for p in P: oczek*=(p-len({0,g%p}))
        ok_crt = sum(v)==oczek==tot
        mom=[]
        for k in range(1,kmax+1):
            lewa=sum(comb(J-1,k)*v[J-1] for J in range(1,len(v)+1)); mom.append(lewa==moment(g,k,P))
        print(f'   luka {g}: suma CRT {"ZGODNA" if ok_crt else "ROZNA !!!"}; momenty k=1..{kmax}: {"ZGODNE" if all(mom) else "ROZNE !!! "+str(mom)}; n_(g,1) = {v[0]}, długości 1..{len(v)}')
if __name__=='__main__':
    kontrola(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv)>3 else 4)

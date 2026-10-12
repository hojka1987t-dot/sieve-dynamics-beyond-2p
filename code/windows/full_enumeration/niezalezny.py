import numpy as np, time
H={2:2,3:6,4:8,5:12,6:16,7:20}
def pierwsze(n):
    p=[];x=2
    while len(p)<n:
        if all(x%d for d in p if d*d<=x): p.append(x)
        x+=1
    return p
print("1) OSTRA DRABINA wprost na cyklach G(N): najmniejsza rozpietosc r ocalalych z jednej klasy mod q")
for k in (4,5,6,7):
    pr=pierwsze(k+1); N=int(np.prod(pr[:k])); q=pr[k]
    L=N*q+20*q*q                                   # wzor ocalalych i klas mod q ma okres N*q
    a=np.arange(L,dtype=np.int64); s=np.ones(L,bool)
    for p in pr[:k]: s[a%p==0]=False
    pos=a[s]; wyn={}
    for r in range(2,8):
        best=None
        for c in range(q):
            v=pos[pos%q==c]
            if v.size>=r:
                m=int((v[r-1:]-v[:v.size-r+1]).min())
                best=m if best is None else min(best,m)
        if best is not None and best<N*q: wyn[r]=best
    zg=all(wyn[r]==q*H[r] for r in wyn)
    print(f"   N={N:>7} q={q}: " + "  ".join(f"r={r}: {wyn[r]} (qH={q*H[r]})" for r in wyn) + f"   -> {'ZGODNE' if zg else 'ROZNE'}")
print("\n2) TWIERDZENIE CZESCIOWE wprost na kolach (wszystkie polozenia, bez klas i bez S(n))")
for r in (5,6,7):
    pr=pierwsze(r+1); P=int(np.prod(pr[:r])); q=pr[r]; P1=P*q; ymax=8*q
    t0=time.time()
    def licz(Pm, prs):
        L=Pm+ymax+2; a=np.arange(L,dtype=np.int64); s=np.ones(L,np.int32)
        for p in prs: s[a%p==0]=0
        return np.concatenate(([0],np.cumsum(s,dtype=np.int32)))
    cs0=licz(P,pr[:r]); cs1=licz(P1,pr[:r+1])
    rek_ok=plus_ok=n6=n8=0
    for y in range(2,ymax,2):
        n0=cs0[y+1:y+1+P]-cs0[:P]; W0=int(n0.min())
        n1=cs1[y+1:y+1+P1]-cs1[:P1]; W1=int(n1.min())
        if W0==0: continue
        anc=n0[np.nonzero(n1==W1)[0]%P]-W0         # przodkowie wszystkich optimow bazy r+1
        if y<6*q: n6+=1; rek_ok+= int(anc.min()==0)
        n8+=1; plus_ok+= int(anc.min()<=1)
    print(f"   baza {r}->{r+1} (q={q}): y<6q: dokladna rekurencja {rek_ok}/{n6};  y<8q: prawo +1 {plus_ok}/{n8}   ({time.time()-t0:.0f} s)")

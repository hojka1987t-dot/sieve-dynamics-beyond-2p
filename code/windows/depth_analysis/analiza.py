import numpy as np, itertools, time, sys, json
def licz(pr, q, ymax, limit):
    N=int(np.prod(pr)); a=np.arange(N+ymax+2,dtype=np.int64); s=np.ones(a.size,bool)
    for p in pr: s&=(a%p!=0)
    cs=np.concatenate(([0],np.cumsum(s,dtype=np.int32)))
    csk=[np.concatenate(([0],np.cumsum(s&(a%q==r),dtype=np.int32))) for r in range(q)]
    ps=pr[1:]; nmax=ymax//(2*q)+2; t=np.arange(nmax); best=np.zeros(nmax,int)
    for wyb in itertools.product(*[range(p) for p in ps]):
        ok=np.ones(nmax,bool)
        for p,c in zip(ps,wyb): ok&=(t%p!=c)
        best=np.maximum(best,np.cumsum(ok))
    S=np.concatenate(([0],best)); x=np.arange(N); wyn=[]; t0=time.time()
    for y in range(2*q, ymax+1, 2):
        n_=cs[x+y+1]-cs[x]; W=int(n_.min())
        if W==0: continue
        mk=np.max(np.stack([c[x+y+1]-c[x] for c in csk]),axis=0)
        C=[]
        for j in range(5):
            sel=n_==W+j
            C.append(int(mk[sel].max()) if sel.any() else -99)
        val=[j-C[j] for j in range(5)]; d=val.index(min(val))
        n=y//(2*q)+1; wyn.append((y,n,int(S[n]),int(S[n]>S[n-1]),W,C[0],C[1],C[2],d))
        if time.time()-t0>limit: break
    return wyn
if __name__=='__main__':
    pr=json.loads(sys.argv[1]); q=int(sys.argv[2]); lim=float(sys.argv[3])
    w=licz(pr,q,3000,lim); json.dump(w,open(f'dane_q{q}.json','w'))
    print(f'q={q}: {len(w)} dlugosci, ostatnia y={w[-1][0]}')

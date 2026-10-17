import numpy as np, time
LIM=10**9; SEG=10**8; S=104; START=47**2
t0=time.time()
mal=np.ones(31624,bool); mal[:2]=False
for i in range(2,178):
    if mal[i]: mal[i*i::i]=False
P=np.nonzero(mal)[0].astype(np.int64)
A2={}; A3={}; ost=[]
for lo in range(0,LIM,SEG):
    hi=min(lo+SEG,LIM); s=np.ones(hi-lo,bool)
    if lo==0: s[:2]=False
    for p in P:
        if p*p>=hi: break
        st=max(p*p,((lo+p-1)//p)*p); s[st-lo::p]=False
    pr=np.nonzero(s)[0].astype(np.int64)+lo
    pr=np.concatenate((np.array(ost,dtype=np.int64),pr)); g=np.diff(pr); a=pr[:-1]
    # pary i trojki kolejnych luk zaczynajace sie od liczby pierwszej >= START
    n=len(g)
    if n>=3:
        a0=a[:n-2]; g1,g2,g3=g[:n-2],g[1:n-1],g[2:n]; ok=a0>=START
        m2=ok&(g1+g2<=S); k2=(g1[m2]//2)*64+g2[m2]//2
        u,c=np.unique(k2,return_counts=True)
        for x,y in zip(u.tolist(),c.tolist()): A2[x]=A2.get(x,0)+y
        m3=ok&(g1+g2+g3<=S); k3=(g1[m3]//2)*4096+(g2[m3]//2)*64+g3[m3]//2
        u,c=np.unique(k3,return_counts=True)
        for x,y in zip(u.tolist(),c.tolist()): A3[x]=A3.get(x,0)+y
    ost=pr[-3:].tolist()                          # zakladka: ostatnie 3 liczby pierwsze do nastepnego segmentu
np.savez('konst104_1e9.npz',A2=np.array(sorted(A2.items())),A3=np.array(sorted(A3.items())))
print(f'sito konstelacji do 1e9: {time.time()-t0:.0f} s; wzorów par: {len(A2)}, trójek: {len(A3)}; par łącznie {sum(A2.values())}, trójek {sum(A3.values())}')

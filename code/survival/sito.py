import numpy as np, time
LIM=10**9; SEG=10**8
t0=time.time()
mal=np.ones(31623+1,bool); mal[:2]=False
for i in range(2,178):
    if mal[i]: mal[i*i::i]=False
P=np.nonzero(mal)[0].astype(np.int64)          # liczby pierwsze do 31623 (do sita i jako p_k przedzialow)
kw=P*P                                          # p_k^2: granice przedzialow przetrwania
K=len(P); G=410
cnt=np.zeros((K,G//2+1),np.int64); ile=np.zeros(K,np.int64); maxg=np.zeros(K,np.int64)
pierwsze={}; ost=None
for lo in range(0,LIM,SEG):
    hi=min(lo+SEG,LIM); s=np.ones(hi-lo,bool)
    if lo==0: s[:2]=False
    for p in P:
        if p*p>=hi: break
        st=max(p*p,((lo+p-1)//p)*p); s[st-lo::p]=False
    pr=np.nonzero(s)[0].astype(np.int64)+lo
    if ost is not None: pr=np.concatenate(([ost],pr))
    g=np.diff(pr); a=pr[:-1]; ost=int(pr[-1])
    k=np.searchsorted(kw,a,side='right')-1        # przedzial [p_k^2, p_{k+1}^2) zawierajacy a
    ok=(k>=0)&(g<=G)
    np.add.at(cnt,(k[ok],g[ok]//2),1); np.add.at(ile,k[k>=0],1); np.maximum.at(maxg,k[k>=0],g[k>=0])
    for gg in np.unique(g):
        if int(gg) not in pierwsze: pierwsze[int(gg)]=int(a[np.argmax(g==gg)])
np.savez('sito_1e9.npz',P=P,cnt=cnt,ile=ile,maxg=maxg,pg=np.array(sorted(pierwsze.items())))
print(f'sito do 1e9: {time.time()-t0:.0f} s; przedziałów przetrwania z danymi: {int((ile>0).sum())}, najwieksza luka: {max(pierwsze)}')

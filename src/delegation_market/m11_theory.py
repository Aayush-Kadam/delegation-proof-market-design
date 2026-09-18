"""Generic-alpha 4x3 deterministic Hedge model for M11."""
from __future__ import annotations

import math


def matrices(v, alpha):
    high=[0,v/2,v,1];low=[0,v/2,v];uh=[];ul=[];rev=[];alloc=[]
    ranks_h=[0,.5,1,2];ranks_l=[0,.5,1]
    for i,bh in enumerate(high):
        rh=[];rl=[];rr=[];ra=[]
        for j,bl in enumerate(low):
            ph=1. if ranks_h[i]>ranks_l[j] else (.5 if ranks_h[i]==ranks_l[j] else 0.);pl=1-ph
            top=max(bh,bl);second=min(bh,bl);price=second+alpha*(top-second)
            rh.append(ph*(1-price));rl.append(pl*(v-price));rr.append(price);ra.append(ph)
        uh.append(rh);ul.append(rl);rev.append(rr);alloc.append(ra)
    return uh,ul,rev,alloc


def soft(logw):
    m=max(logw);w=[math.exp(x-m) for x in logw];s=sum(w);return[x/s for x in w]


def run(v,eta_h,eta_l,horizon,alpha):
    uh,ul,rev,alloc=matrices(v,alpha);lh=[0.]*4;ll=[0.]*3;sr=sa=0.
    for _ in range(horizon):
        q=soft(lh);p=soft(ll)
        sr+=sum(q[i]*p[j]*rev[i][j] for i in range(4) for j in range(3))
        sa+=sum(q[i]*p[j]*alloc[i][j] for i in range(4) for j in range(3))
        euh=[sum(uh[i][j]*p[j] for j in range(3)) for i in range(4)]
        eul=[sum(q[i]*ul[i][j] for i in range(4)) for j in range(3)]
        lh=[lh[i]+eta_h*euh[i] for i in range(4)];ll=[ll[j]+eta_l*eul[j] for j in range(3)]
    return sr/horizon,sa/horizon


def derivative(v,eta_h,eta_l,horizon,alpha,step=1e-5):
    lo=max(0,alpha-step);hi=min(1,alpha+step)
    r0,a0=run(v,eta_h,eta_l,horizon,lo);r1,a1=run(v,eta_h,eta_l,horizon,hi)
    return (r1-r0)/(hi-lo),(a1-a0)/(hi-lo)


def threshold(v,eta_h,eta_l,horizon,objective,target,tol=1e-12):
    increasing=objective=="revenue";lo,hi=0.,1.
    for _ in range(80):
        mid=(lo+hi)/2;r,a=run(v,eta_h,eta_l,horizon,mid);value=r if increasing else a
        if (value>=target)==increasing: hi=mid
        else: lo=mid
    return (lo+hi)/2

"""Outward Decimal interval/dual certificate for the M11 alpha witness."""
from __future__ import annotations
from decimal import Decimal as D,getcontext
import json
from pathlib import Path
getcontext().prec=70

def I(a,b=None):return(D(str(a)),D(str(a if b is None else b)))
def dn(x):return x.next_minus()
def up(x):return x.next_plus()
def add(a,b):return dn(a[0]+b[0]),up(a[1]+b[1])
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 z=[a[i]*b[j] for i in(0,1)for j in(0,1)];return dn(min(z)),up(max(z))
def inv(a):
 if a[0]<=0<=a[1]:raise ZeroDivisionError
 z=[D(1)/a[0],D(1)/a[1]];return dn(min(z)),up(max(z))
def div(a,b):return mul(a,inv(b))
def ex(a):return dn(a[0].exp()),up(a[1].exp())
def sumiv(xs):
 s=I(0)
 for x in xs:s=add(s,x)
 return s

# Dual interval is (value interval, derivative interval).
def C(x):return(I(x),I(0))
def V(x,dx=1):return(x,I(dx))
def da(x,y):return add(x[0],y[0]),add(x[1],y[1])
def dn_(x):return neg(x[0]),neg(x[1])
def ds(x,y):return da(x,dn_(y))
def dm(x,y):return mul(x[0],y[0]),add(mul(x[1],y[0]),mul(x[0],y[1]))
def di(x,y):return dm(x,(inv(y[0]),neg(div(y[1],mul(y[0],y[0])))))
def de(x):return ex(x[0]),mul(ex(x[0]),x[1])
def dsum(xs):
 s=C(0)
 for x in xs:s=da(s,x)
 return s
def soft(xs):
 e=[de(x)for x in xs];s=dsum(e);return[di(x,s)for x in e]

def run(alpha):
 one=C(1);zero=C(0);v0=D(1)/D(3);v=(v0.next_minus(),v0.next_plus());vD=V(v,0)
 high=[zero,dm(vD,C('.5')),vD,one];low=[zero,dm(vD,C('.5')),vD]
 ranks_h=[0,.5,1,2];ranks_l=[0,.5,1];uh=[];ul=[];rv=[];alloc=[]
 for i,bh in enumerate(high):
  rh=[];rl=[];rr=[];ra=[]
  for j,bl in enumerate(low):
   ph=C(1 if ranks_h[i]>ranks_l[j] else (.5 if ranks_h[i]==ranks_l[j] else 0));pl=ds(one,ph)
   top=bh if ranks_h[i]>=ranks_l[j] else bl;second=bl if ranks_h[i]>=ranks_l[j] else bh
   price=da(second,dm(alpha,ds(top,second)))
   rh.append(dm(ph,ds(one,price)));rl.append(dm(pl,ds(vD,price)));rr.append(price);ra.append(ph)
  uh.append(rh);ul.append(rl);rv.append(rr);alloc.append(ra)
 lh=[zero]*4;ll=[zero]*3;sr=zero;sa=zero
 for _ in range(9):
  q=soft(lh);p=soft(ll);sr=da(sr,dsum([dm(dm(q[i],p[j]),rv[i][j])for i in range(4)for j in range(3)]));sa=da(sa,dsum([dm(dm(q[i],p[j]),alloc[i][j])for i in range(4)for j in range(3)]))
  euh=[dsum([dm(uh[i][j],p[j])for j in range(3)])for i in range(4)];eul=[dsum([dm(q[i],ul[i][j])for i in range(4)])for j in range(3)]
  lh=[da(lh[i],dm(C(4),euh[i]))for i in range(4)];ll=ll  # eta_L=0
 return dm(sr,C(D(1)/D(9))),dm(sa,C(D(1)/D(9)))

def certify(output:Path,parts=10_000):
 deriv=[]
 for k in range(parts):
  lo=D(k)/D(parts);hi=D(k+1)/D(parts);r,a=run(V((lo,hi)));deriv.append((r[1],a[1]))
 dr=(min(x[0][0]for x in deriv),max(x[0][1]for x in deriv));da_=(min(x[1][0]for x in deriv),max(x[1][1]for x in deriv))
 r0,a0=run(V(I(0)));r1,a1=run(V(I(1)));midr=dm(da(r0,r1),C('.5'));mida=dm(da(a0,a1),C('.5'))
 r36,a36=run(V(I('.36')));r37,a37=run(V(I('.37')));r21,a21=run(V(I('.21')));r22,a22=run(V(I('.22')))
 checks={"revenue_strictly_increasing":dr[0]>0,"allocation_strictly_decreasing":da_[1]<0,
         "revenue_at_036_below_midpoint":r36[0][1]<midr[0][0],"revenue_at_037_above_midpoint":r37[0][0]>midr[0][1],
         "allocation_at_021_above_midpoint":a21[0][0]>mida[0][1],"allocation_at_022_below_midpoint":a22[0][1]<mida[0][0]}
 data={"witness":{"v":"1/3","eta_high":"4","eta_low":"0","H":9},"alpha_subintervals":parts,
       "revenue_derivative":[str(x)for x in dr],"allocation_derivative":[str(x)for x in da_],
       "R0":[str(x)for x in r0[0]],"R1":[str(x)for x in r1[0]],"A0":[str(x)for x in a0[0]],"A1":[str(x)for x in a1[0]],
       "revenue_midpoint":[str(x)for x in midr[0]],"allocation_midpoint":[str(x)for x in mida[0]],
       "R_036":[str(x)for x in r36[0]],"R_037":[str(x)for x in r37[0]],"A_021":[str(x)for x in a21[0]],"A_022":[str(x)for x in a22[0]],
       "checks":checks,"certified":all(checks.values()),"method":f"70-digit outward Decimal interval automatic differentiation over {parts} exhaustive alpha subintervals."}
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(data,indent=2)+'\n');return data

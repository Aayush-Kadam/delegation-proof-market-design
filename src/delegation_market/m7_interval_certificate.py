"""Outward interval certificate for the M7 4x2 rectangle."""
from decimal import Decimal as D,getcontext
import argparse,json
from pathlib import Path
getcontext().prec=70
def I(a,b=None):return(D(str(a)),D(str(a if b is None else b)))
def dn(x):return x.next_minus()
def up(x):return x.next_plus()
def add(a,b):return dn(a[0]+b[0]),up(a[1]+b[1])
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 z=[a[i]*b[j] for i in (0,1) for j in (0,1)];return dn(min(z)),up(max(z))
def inv(a):return dn(D(1)/a[1]),up(D(1)/a[0])
def div(a,b):return mul(a,inv(b))
def ex(a):return dn(a[0].exp()),up(a[1].exp())
def sc(a,c):return mul(a,I(c))
def state(x,y,r,z):
 e=[I(1),ex(r),ex(add(r,y)),ex(add(add(r,y),x))];d=add(add(e[0],e[1]),add(e[2],e[3]));q=[div(t,d) for t in e];p=div(ex(z),add(I(1),ex(z)));return q,p
def step(v,eh,el,m,x,y,r,z):
 q,p=state(x,y,r,z);u0=sc(sub(I(1),p),'.5')
 if m=='FPA':uh=mul(sub(I(1),p),sub(I(1),sc(v,'.5')));uv=mul(sub(I(1),v),sub(I(1),sc(p,'.5')));u1=I(0);z2=sub(z,sc(mul(mul(el,v),q[0]),'.5'))
 else:uh=sub(I(1),p);uv=sub(I(1),sc(mul(p,add(I(1),v)),'.5'));u1=sub(I(1),mul(v,p));z2=add(z,sc(mul(mul(el,v),add(q[0],q[1])),'.5'))
 return add(x,mul(eh,sub(u1,uv))),add(y,mul(eh,sub(uv,uh))),add(r,mul(eh,sub(uh,u0))),z2
def met(v,m,q,p):
 a=add(add(sc(mul(q[0],sub(I(1),p)),'.5'),mul(add(q[1],q[2]),sub(I(1),sc(p,'.5')))),q[3])
 rf=add(add(add(sc(mul(v,q[1]),'.5'),mul(v,q[2])),q[3]),mul(mul(p,v),q[0]))
 rs=add(mul(mul(v,p),add(q[2],q[3])),sc(mul(mul(v,p),q[1]),'.5'))
 return (rf if m=='FPA' else rs),a
def run(v,eh,el,H,m):
 x=y=r=z=I(0);sr=sa=I(0)
 for _ in range(H):q,p=state(x,y,r,z);rr,a=met(v,m,q,p);sr=add(sr,rr);sa=add(sa,a);x,y,r,z=step(v,eh,el,m,x,y,r,z)
 return sc(sr,D(1)/D(H)),sc(sa,D(1)/D(H))
def cert(out):
 vs=[D('.30')+D('.06')*D(i)/12 for i in range(13)];hs=[D('.8')+D('.4')*D(i)/8 for i in range(9)];ls=[D('.05')+D('.10')*D(i)/5 for i in range(6)];agg={h:[None]*4 for h in range(2,10)}
 for i in range(12):
  for j in range(8):
   for k in range(5):
    v=(vs[i],vs[i+1]);eh=(hs[j],hs[j+1]);el=(ls[k],ls[k+1])
    for h in agg:
     rf,af=run(v,eh,el,h,'FPA');rs,ass=run(v,eh,el,h,'SPA');dr=sub(rf,rs);da=sub(ass,af);a=agg[h]
     for n,val in enumerate((dr[0],dr[1],da[0],da[1])):a[n]=val if a[n] is None else (min(a[n],val) if n%2==0 else max(a[n],val))
 rows=[{'H':h,'revenue_gap':[str(a[0]),str(a[1])],'allocation_gap':[str(a[2]),str(a[3])],'certified':a[0]>0 and a[2]>0}for h,a in agg.items()]
 d={'box':{'v':['.30','.36'],'eta_high':['.8','1.2'],'eta_low':['.05','.15']},'subboxes':480,'rows':rows,'method':'70-digit outward Decimal intervals over exhaustive 12x8x5 subdivision.'};out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2));assert all(r['certified'] for r in rows if r['H']<=6)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);cert(p.parse_args().output)

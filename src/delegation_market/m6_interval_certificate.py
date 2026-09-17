"""Directed enclosure certificate using Decimal adjacent representables."""
from decimal import Decimal as D, getcontext
import argparse,json
from pathlib import Path
getcontext().prec=70
def down(x): return x.next_minus()
def up(x): return x.next_plus()
def I(a,b=None): return (D(str(a)),D(str(a if b is None else b)))
def add(a,b): return down(a[0]+b[0]),up(a[1]+b[1])
def neg(a): return -a[1],-a[0]
def sub(a,b): return add(a,neg(b))
def mul(a,b):
 z=[a[i]*b[j] for i in (0,1) for j in (0,1)];return down(min(z)),up(max(z))
def inv(a): assert a[0]>0;return down(D(1)/a[1]),up(D(1)/a[0])
def div(a,b): return mul(a,inv(b))
def expiv(a): return down(a[0].exp()),up(a[1].exp())
def scale(a,c): return mul(a,I(c))
def sigmoid(a): return div(expiv(a),add(I(1),expiv(a)))
def state(x,y,z):
 e0=I(1);ev=expiv(y);e1=expiv(add(x,y));den=add(add(e0,ev),e1)
 return [div(e0,den),div(ev,den),div(e1,den)],sigmoid(z)
def step(v,eh,el,m,x,y,z):
 q,p=state(x,y,z);u0=scale(sub(I(1),p),'.5')
 if m=='FPA':uv=mul(sub(I(1),v),sub(I(1),scale(p,'.5')));u1=I(0);z=sub(z,scale(mul(mul(el,v),q[0]),'.5'))
 else:uv=sub(I(1),scale(mul(p,add(I(1),v)),'.5'));u1=sub(I(1),mul(v,p));z=add(z,scale(mul(mul(el,v),q[0]),'.5'))
 return add(x,mul(eh,sub(u1,uv))),add(y,mul(eh,sub(uv,u0))),z
def metrics(v,m,q,p):
 a=add(add(scale(mul(q[0],sub(I(1),p)),'.5'),mul(q[1],sub(I(1),scale(p,'.5')))),q[2])
 r=add(mul(v,add(q[1],mul(p,q[0]))),q[2]) if m=='FPA' else mul(mul(v,p),add(q[1],q[2]))
 return r,a
def run(v,eh,el,H,m):
 x=y=z=I(0);sr=sa=I(0)
 for _ in range(H):
  q,p=state(x,y,z);r,a=metrics(v,m,q,p);sr=add(sr,r);sa=add(sa,a);x,y,z=step(v,eh,el,m,x,y,z)
 return scale(sr,D(1)/D(H)),scale(sa,D(1)/D(H))
def cert(out):
 # Subdivision controls dependency inflation while covering the full closed box.
 vs=[D('.30')+D('.06')*D(i)/12 for i in range(13)]
 hs=[D('.8')+D('.4')*D(i)/8 for i in range(9)]
 ls=[D('.05')+D('.10')*D(i)/5 for i in range(6)]
 agg={H:[None,None,None,None] for H in range(2,11)}
 for i in range(12):
  for j in range(8):
   for k in range(5):
    v=(vs[i],vs[i+1]);eh=(hs[j],hs[j+1]);el=(ls[k],ls[k+1])
    for H in range(2,11):
     rf,af=run(v,eh,el,H,'FPA');rs,ass=run(v,eh,el,H,'SPA');dr=sub(rf,rs);da=sub(ass,af)
     a=agg[H];a[0]=dr[0] if a[0] is None else min(a[0],dr[0]);a[1]=dr[1] if a[1] is None else max(a[1],dr[1]);a[2]=da[0] if a[2] is None else min(a[2],da[0]);a[3]=da[1] if a[3] is None else max(a[3],da[1])
 rows=[{'H':H,'revenue_gap':[str(a[0]),str(a[1])],'allocation_gap':[str(a[2]),str(a[3])],'certified':a[0]>0 and a[2]>0} for H,a in agg.items()]
 data={'box':{'v':['0.30','0.36'],'eta_high':['0.8','1.2'],'eta_low':['0.05','0.15']},'rows':rows,
 'subboxes':480,'method':'70-digit Decimal interval propagation over 12x8x5 exhaustive subdivision; every elementary result expanded to adjacent representable decimals; Decimal.exp is correctly rounded.'}
 out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print(json.dumps(data,indent=2));assert all(x['certified'] for x in rows if x['H']<=9)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);cert(p.parse_args().output)

"""Outward interval certification for the 4x3 auction generated from rules."""
from decimal import Decimal as D,getcontext
import json,argparse
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
def inv(a):return dn(D(1)/a[1]),up(D(1)/a[0])
def div(a,b):return mul(a,inv(b))
def ex(a):return dn(a[0].exp()),up(a[1].exp())
def sc(a,c):return mul(a,I(c))
def sumiv(xs):
 s=I(0)
 for x in xs:s=add(s,x)
 return s
def soft(logw):
 e=[ex(x) for x in logw];s=sumiv(e);return[div(x,s)for x in e]
def mats(v,m):
 hb=[I(0),sc(v,'.5'),v,I(1)];lb=[I(0),sc(v,'.5'),v];uh=[];ul=[];rv=[];al=[]
 ranksH=[0,.5,1,2];ranksL=[0,.5,1]
 for i,bh in enumerate(hb):
  RH=[];RL=[];RR=[];RA=[]
  for j,bl in enumerate(lb):
   ph=I(1 if ranksH[i]>ranksL[j] else (.5 if ranksH[i]==ranksL[j] else 0));pl=sub(I(1),ph)
   if m=='FPA':RH.append(mul(ph,sub(I(1),bh)));RL.append(mul(pl,sub(v,bl)));RR.append(add(mul(ph,bh),mul(pl,bl)))
   else:RH.append(mul(ph,sub(I(1),bl)));RL.append(mul(pl,sub(v,bh)));RR.append(bl if ranksH[i]>=ranksL[j] else bh)
   RA.append(ph)
  uh.append(RH);ul.append(RL);rv.append(RR);al.append(RA)
 return uh,ul,rv,al
def run(v,eh,el,H,m):
 uh,ul,rv,al=mats(v,m);lh=[I(0)]*4;ll=[I(0)]*3;sr=sa=I(0)
 for _ in range(H):
  q=soft(lh);p=soft(ll);sr=add(sr,sumiv([mul(mul(q[i],p[j]),rv[i][j])for i in range(4)for j in range(3)]));sa=add(sa,sumiv([mul(mul(q[i],p[j]),al[i][j])for i in range(4)for j in range(3)]))
  euh=[sumiv([mul(uh[i][j],p[j])for j in range(3)])for i in range(4)];eul=[sumiv([mul(q[i],ul[i][j])for i in range(4)])for j in range(3)]
  lh=[add(lh[i],mul(eh,euh[i]))for i in range(4)];ll=[add(ll[j],mul(el,eul[j]))for j in range(3)]
 return sc(sr,D(1)/D(H)),sc(sa,D(1)/D(H))
def cert(out):
 vs=[D('.30')+D('.06')*D(i)/12 for i in range(13)];hs=[D('.8')+D('.4')*D(i)/8 for i in range(9)];ls=[D('.05')+D('.10')*D(i)/5 for i in range(6)];agg={h:[None]*4 for h in range(2,7)}
 for i in range(12):
  for j in range(8):
   for k in range(5):
    v=(vs[i],vs[i+1]);eh=(hs[j],hs[j+1]);el=(ls[k],ls[k+1])
    for h in agg:
     rf,af=run(v,eh,el,h,'FPA');rs,ass=run(v,eh,el,h,'SPA');vals=(sub(rf,rs)[0],sub(rf,rs)[1],sub(ass,af)[0],sub(ass,af)[1]);a=agg[h]
     for n,val in enumerate(vals):a[n]=val if a[n]is None else(min(a[n],val)if n%2==0 else max(a[n],val))
 rows=[{'H':h,'revenue_gap':[str(a[0]),str(a[1])],'allocation_gap':[str(a[2]),str(a[3])],'certified':a[0]>0 and a[2]>0}for h,a in agg.items()]
 d={'box':{'v':['.30','.36'],'eta_high':['.8','1.2'],'eta_low':['.05','.15']},'subboxes':480,'rows':rows,'method':'Rule-generated payoff matrices; 70-digit outward Decimal intervals; exhaustive 12x8x5 subdivision.'};out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2));assert all(x['certified']for x in rows if x['H']<=5)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);cert(p.parse_args().output)

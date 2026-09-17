"""Deterministic exact-payoff 4x3 Hedge model for M8."""
import math,csv,json,argparse
from fractions import Fraction
from pathlib import Path
def matrices(v,m):
 half=Fraction(1,2) if isinstance(v,Fraction) else .5
 H=[0,v/2,v,1];L=[0,v/2,v];uh=[];ul=[];rev=[];alloc=[]
 for bh in H:
  rh=[];rl=[];rr=[];ra=[]
  for bl in L:
   ph=1 if bh>bl else (half if bh==bl else 0);pl=1-ph
   if m=='FPA': rh.append(ph*(1-bh));rl.append(pl*(v-bl));rr.append(ph*bh+pl*bl)
   else:rh.append(ph*(1-bl));rl.append(pl*(v-bh));rr.append(min(bh,bl))
   ra.append(ph)
  uh.append(rh);ul.append(rl);rev.append(rr);alloc.append(ra)
 return uh,ul,rev,alloc
def soft(logw):
 m=max(logw);w=[math.exp(x-m) for x in logw];s=sum(w);return[x/s for x in w]
def run(v,eh,el,T,m):
 uh,ul,rev,alloc=matrices(v,m);lh=[0.]*4;ll=[0.]*3;sr=sa=0.
 for _ in range(T):
  q=soft(lh);p=soft(ll)
  sr+=sum(q[i]*p[j]*rev[i][j] for i in range(4) for j in range(3));sa+=sum(q[i]*p[j]*alloc[i][j] for i in range(4) for j in range(3))
  euH=[sum(uh[i][j]*p[j] for j in range(3)) for i in range(4)];euL=[sum(q[i]*ul[i][j] for i in range(4)) for j in range(3)]
  lh=[lh[i]+eh*euH[i] for i in range(4)];ll=[ll[j]+el*euL[j] for j in range(3)]
 return sr/T,sa/T
def contrast(v,eh,el,H):
 rf,af=run(v,eh,el,H,'FPA');rs,ass=run(v,eh,el,H,'SPA');return {'v':v,'eta_high':eh,'eta_low':el,'H':H,'delta_revenue':rf-rs,'delta_allocation':ass-af,'conflict':rf>rs and ass>af}
def analyze(out):
 out.mkdir(parents=True,exist_ok=True);rows=[]
 for v in (.30,.32,1/3,.34,.36):
  for eh in (.8,.9,1,1.1,1.2):
   for el in (.05,.075,.1,.125,.15):
    for H in range(2,7):rows.append(contrast(v,eh,el,H))
 with(out/'reconnaissance.csv').open('w',newline='',encoding='utf8')as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 d={'configurations':125,'evaluations':625,'all_conflict':all(x['conflict'] for x in rows),'witness':[contrast(1/3,1,.1,h) for h in range(2,7)]};(out/'exploration.json').write_text(json.dumps(d,indent=2)+'\n');return d
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);print(json.dumps(analyze(p.parse_args().output),indent=2))

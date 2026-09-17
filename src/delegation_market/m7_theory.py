"""Deterministic 4x2 Hedge recurrence for M7."""
import math,csv,json,argparse
from pathlib import Path
def sig(z):
 e=math.exp(-abs(z));return 1/(1+e) if z>=0 else e/(1+e)
def state(x,y,r,z):
 a=[0,r,r+y,r+y+x];m=max(a);w=[math.exp(t-m) for t in a];s=sum(w)
 return [t/s for t in w],sig(z)
def step(v,eh,el,m,x,y,r,z):
 q,p=state(x,y,r,z);u0=(1-p)/2
 if m=='FPA':
  uh=(1-p)*(1-v/2);uv=(1-v)*(1-p/2);u1=0;z2=z-el*v*q[0]/2
 else:
  uh=1-p;uv=1-p*(1+v)/2;u1=1-v*p;z2=z+el*v*(q[0]+q[1])/2
 return x+eh*(u1-uv),y+eh*(uv-uh),r+eh*(uh-u0),z2
def metrics(v,m,q,p):
 a=q[0]*(1-p)/2+(q[1]+q[2])*(1-p/2)+q[3]
 if m=='FPA':r=v/2*q[1]+v*q[2]+q[3]+p*v*q[0]
 else:r=v*p*(q[2]+q[3])+v*p*q[1]/2
 return r,a
def run(v,eh,el,H,m):
 x=y=r=z=0.;sr=sa=0.
 for _ in range(H):
  q,p=state(x,y,r,z);rr,a=metrics(v,m,q,p);sr+=rr;sa+=a;x,y,r,z=step(v,eh,el,m,x,y,r,z)
 return sr/H,sa/H
def contrast(v,eh,el,H):
 rf,af=run(v,eh,el,H,'FPA');rs,ass=run(v,eh,el,H,'SPA')
 return {'v':v,'eta_high':eh,'eta_low':el,'H':H,'delta_revenue':rf-rs,'delta_allocation':ass-af,'conflict':rf>rs and ass>af}
def analyze(out):
 out.mkdir(parents=True,exist_ok=True);rows=[]
 for v in (.30,.32,1/3,.34,.36):
  for eh in (.8,.9,1,1.1,1.2):
   for el in (.05,.075,.1,.125,.15):
    for H in range(2,10):rows.append(contrast(v,eh,el,H))
 with (out/'reconnaissance.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 d={'configurations':125,'evaluations':len(rows),'all_conflict':all(x['conflict'] for x in rows),'witness':[contrast(1/3,1,.1,h) for h in range(2,10)]}
 (out/'exploration.json').write_text(json.dumps(d,indent=2)+'\n');return d
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);print(json.dumps(analyze(p.parse_args().output),indent=2))

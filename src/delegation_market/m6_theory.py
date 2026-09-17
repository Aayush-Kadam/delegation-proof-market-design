"""Exact recurrence evaluation for the M6 3x2 Hedge model."""
from __future__ import annotations
import math, csv, json, argparse
from pathlib import Path

def sigmoid(z):
    if z>=0: return 1/(1+math.exp(-z))
    e=math.exp(z); return e/(1+e)

def state(x,y,z):
    # x=log(w1/wv), y=log(wv/w0), z=log(wLv/wL0)
    a=[0,y,x+y]; m=max(a); w=[math.exp(t-m) for t in a]; s=sum(w)
    return [t/s for t in w], sigmoid(z)

def step(v,eh,el,mechanism,x,y,z):
    q,p=state(x,y,z); q0=q[0]
    u0=(1-p)/2
    if mechanism=='FPA':
        uv=(1-v)*(1-p/2); u1=0
        z2=z-el*v*q0/2
    else:
        uv=1-p*(1+v)/2; u1=1-v*p
        z2=z+el*v*q0/2
    return x+eh*(u1-uv), y+eh*(uv-u0), z2

def metrics(v,mechanism,q,p):
    alloc=q[0]*(1-p)/2+q[1]*(1-p/2)+q[2]
    rev=v*(q[1]+p*q[0])+q[2] if mechanism=='FPA' else v*p*(q[1]+q[2])
    return rev,alloc

def run(v,eh,el,H,mechanism):
    x=y=z=0.; sr=sa=0.
    for _ in range(H):
        q,p=state(x,y,z); r,a=metrics(v,mechanism,q,p); sr+=r;sa+=a
        x,y,z=step(v,eh,el,mechanism,x,y,z)
    return sr/H,sa/H,(x,y,z)

def contrast(v,eh,el,H):
    rf,af,sf=run(v,eh,el,H,'FPA'); rs,ass,ss=run(v,eh,el,H,'SPA')
    return {'v':v,'eta_high':eh,'eta_low':el,'H':H,'delta_revenue':rf-rs,
            'delta_allocation':ass-af,'conflict':rf>rs and ass>af}

def analyze(out:Path):
    out.mkdir(parents=True,exist_ok=True); rows=[]
    # 7*5*5=175 parameter configurations, each evaluated on one horizon ladder.
    for v in (.28,.30,.32,1/3,.35,.37,.40):
      for eh in (.7,.85,1.,1.15,1.3):
       for el in (.04,.07,.10,.13,.16):
        for H in (2,3,4,5,10,20,50,100): rows.append(contrast(v,eh,el,H))
    with (out/'horizon_ladder.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    witness=[contrast(1/3,1,.1,H) for H in (2,3,4,5,10,20,50,100)]
    verdict={'parameter_configurations':175,'evaluations':len(rows),'witness_ladder':witness,
             'all_box_grid_conflict_through_5':all(r['conflict'] for r in rows if r['H']<=5),
             'first_witness_failure':next((r for r in witness if not r['conflict']),None)}
    (out/'exploration.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
    return verdict

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    print(json.dumps(analyze(p.parse_args().output),indent=2))

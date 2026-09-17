"""Exact-rational interval certificate for TH-M5-003's witness point."""
from fractions import Fraction as F
import json
from pathlib import Path

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    z=[x[i]*y[j] for i in (0,1) for j in (0,1)]
    return min(z),max(z)
def inv(x):
    assert x[0]>0
    return F(1,x[1]),F(1,x[0])
def div(x,y): return mul(x,inv(y))

def exp_pos(x:F,n=40):
    assert x>=0
    term=F(1); s=term
    for k in range(1,n+1):
        term*=x/k; s+=term
    nxt=term*x/(n+1)
    ratio=x/(n+2)
    return s, s+nxt/(1-ratio)
def exp_iv(x:F):
    return exp_pos(x) if x>=0 else inv(exp_pos(-x))
def softmax_iv(xs):
    e=[exp_iv(x) for x in xs]; z=(sum(a for a,b in e),sum(b for a,b in e))
    return [div(a,z) for a in e]

def allocation(q,p):
    one=(F(1),F(1)); half=(F(1,2),F(1,2))
    om=(one[0]-p[1],one[1]-p[0])
    omh=(one[0]-p[1]/2,one[1]-p[0]/2)
    return add(add(mul(q[0],mul(half,om)),mul(q[1],omh)),q[2])

def certify(output:Path):
    v=F(1,3); eh=F(1); el=F(1,10)
    qf=softmax_iv([eh/F(4),3*eh*(1-v)/4,F(0)])
    qs=softmax_iv([eh/F(4),eh*(3-v)/4,eh*(1-v/2)])
    ef=exp_iv(el*v/6); es=exp_iv(-el*v/6)
    pf=inv(add((F(1),F(1)),ef)); ps=inv(add((F(1),F(1)),es))
    af=allocation(qf,pf); ass=allocation(qs,ps)
    phi=(ass[0]-af[1],ass[1]-af[0])
    rev_bound=(2-5*v)/12
    assert phi[0]>0 and rev_bound>0
    data={"point":{"v":"1/3","eta_high":"1","eta_low":"1/10"},
          "phi_interval":[str(phi[0]),str(phi[1])],
          "phi_decimal":[float(phi[0]),float(phi[1])],
          "allocation_gap_interval":[str(phi[0]/2),str(phi[1]/2)],
          "revenue_gap_analytic_lower_bound":str(rev_bound),
          "method":"Exact Fraction arithmetic; exp Taylor partial sum plus geometric remainder bound, 40 terms."}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    return data

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    print(json.dumps(certify(p.parse_args().output),indent=2))

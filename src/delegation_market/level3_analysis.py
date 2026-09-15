"""Protocol-specified paired analysis and candidate detection for Level 3."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd

KEYS=["v_low","horizon","c_high","c_low","step","seed"]
CELL=["v_low","horizon","c_high","c_low","step"]
METRICS=["full_dl_revenue","tail_dl_revenue","full_ndl_revenue","tail_ndl_revenue","full_dl_ae","tail_dl_ae","full_dl_welfare","tail_dl_welfare","full_surplus_high","full_surplus_low","full_surplus_total"]


def paired_frame(df):
    a=df[df.mechanism=="first_price"].set_index(KEYS); b=df[df.mechanism=="second_price"].set_index(KEYS)
    common=a.index.intersection(b.index); out=pd.DataFrame(index=common).reset_index()
    for m in METRICS: out["delta_"+m]=a.loc[common,m].to_numpy()-b.loc[common,m].to_numpy()
    return out


def ci95(x):
    x=np.asarray(x,float); n=len(x); critical=2.045 if n==30 else (2.009 if n==50 else 1.96)
    mean=x.mean(); half=critical*x.std(ddof=1)/math.sqrt(n)
    return mean,mean-half,mean+half


def aggregate_pairs(p):
    rows=[]
    for key,g in p.groupby(CELL):
        r=dict(zip(CELL,key)); r["n_seeds"]=len(g)
        for m in [c for c in p.columns if c.startswith("delta_")]:
            mean,lo,hi=ci95(g[m]); r[m+"_mean"]=mean; r[m+"_ci_low"]=lo; r[m+"_ci_high"]=hi
        rows.append(r)
    return pd.DataFrame(rows)


def detect(cells, raw):
    tau_r,tau_ae,tau_w=.05,.01,.005; found=[]
    rcol="delta_full_ndl_revenue_mean"; lo="delta_full_ndl_revenue_ci_low"; hi="delta_full_ndl_revenue_ci_high"
    sig=cells[((cells[lo]>0)|(cells[hi]<0)) & (cells[rcol].abs()>=tau_r)].copy()
    # C1 valuation reversals within horizon/rates.
    for key,g in sig.groupby(["horizon","c_high","c_low","step"]):
        if (g[rcol]>0).any() and (g[rcol]<0).any():
            found.append({"class":"C1","scope":str(key),"magnitude":float(g[rcol].abs().min()),"support_cells":len(g)})
    # C2 horizon reversals within valuation/rates.
    for key,g in sig.groupby(["v_low","c_high","c_low","step"]):
        if (g[rcol]>0).any() and (g[rcol]<0).any(): found.append({"class":"C2","scope":str(key),"magnitude":float(g[rcol].abs().min()),"support_cells":len(g)})
    # C3 objective conflicts, recorded as strongest cell.
    ae="delta_full_dl_ae_mean"; aelo="delta_full_dl_ae_ci_low"; aehi="delta_full_dl_ae_ci_high"; w="delta_full_dl_welfare_mean"; wlo="delta_full_dl_welfare_ci_low"; whi="delta_full_dl_welfare_ci_high"
    c3=cells[((cells[rcol]*cells[ae]<0)&(cells[rcol].abs()>=tau_r)&(cells[ae].abs()>=tau_ae)&(((cells[lo]>0)&(cells[aehi]<0))|((cells[hi]<0)&(cells[aelo]>0)))) | ((cells[rcol]*cells[w]<0)&(cells[rcol].abs()>=tau_r)&(cells[w].abs()>=tau_w)&(((cells[lo]>0)&(cells[whi]<0))|((cells[hi]<0)&(cells[wlo]>0))))].copy()
    if len(c3):
        c3["joint_magnitude"]=c3[rcol].abs()+c3[ae].abs()+c3[w].abs(); q=c3.sort_values("joint_magnitude",ascending=False).iloc[0]
        found.append({"class":"C3","scope":json.dumps({k:float(q[k]) for k in CELL}),"magnitude":float(abs(q[rcol])),"support_cells":len(c3)})
    # C4 compares mechanism profiles using cell means, not seed pseudoreplication.
    mech=raw.groupby(["mechanism"]+CELL).full_ndl_revenue.mean().reset_index()
    prof=mech.groupby("mechanism").full_ndl_revenue.agg(["mean","median",lambda x:np.quantile(x,.9),"max"]).rename(columns={"<lambda_0>":"p90"})
    if np.sign(prof.loc["first_price","mean"]-prof.loc["second_price","mean"]) != np.sign(prof.loc["first_price","max"]-prof.loc["second_price","max"]):
        mag=min(abs(prof.loc["first_price","mean"]-prof.loc["second_price","mean"]),abs(prof.loc["first_price","max"]-prof.loc["second_price","max"]))
        if mag>=tau_r: found.append({"class":"C4","scope":"all development cells","magnitude":float(mag),"support_cells":len(cells)})
    # C5 adjacent valuation sign boundary.
    for key,g in sig.groupby(["horizon","c_high","c_low","step"]):
        g=g.sort_values("v_low")
        for (_,a),(_,b) in zip(g.iloc[:-1].iterrows(),g.iloc[1:].iterrows()):
            if a[rcol]*b[rcol]<0: found.append({"class":"C5","scope":str(key)+(f" v=({a.v_low},{b.v_low})"),"magnitude":float(min(abs(a[rcol]),abs(b[rcol]))),"support_cells":2})
    base={"C1":(8,7,9,8),"C2":(8,6,9,8),"C3":(6,8,9,9),"C4":(8,7,7,9),"C5":(8,7,8,8)}
    for f in found:
        nov,theory,hold,policy=base[f["class"]]; f["economic_magnitude_score"]=min(10.,10*f["magnitude"]/(2*tau_r)); f["statistical_robustness_score"]=min(10.,5+math.log10(max(1,f["support_cells"]))*3)
        f.update({"novelty_potential_score":nov,"theory_tractability_score":theory,"holdout_testability_score":hold,"policy_relevance_score":policy}); f["total_score"]=sum(v for k,v in f.items() if k.endswith("_score"))
    order={"C1":0,"C2":1,"C3":2,"C4":3,"C5":4}; found.sort(key=lambda f:(-f["total_score"],order[f["class"]],f["scope"]))
    return found,prof.reset_index()


def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",type=Path,required=True); p.add_argument("--output",type=Path,required=True); a=p.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(a.input); paired=paired_frame(raw); cells=aggregate_pairs(paired); found,profile=detect(cells,raw)
    paired.to_csv(a.output/"paired_seed_differences.csv",index=False); cells.to_csv(a.output/"paired_cell_summary.csv",index=False); profile.to_csv(a.output/"robustness_profile.csv",index=False)
    (a.output/"candidate_flags.json").write_text(json.dumps(found,indent=2),encoding="utf-8"); print(json.dumps(found[:10],indent=2))
if __name__=="__main__": main()

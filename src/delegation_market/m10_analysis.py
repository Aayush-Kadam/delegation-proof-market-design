"""Frozen completeness and development-gate analysis for M10."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from delegation_market.level3 import _atomic_json, file_hash
from delegation_market.m10 import run_id, tasks


def validate(root, config):
    expected=tasks(root,config); expected_ids={run_id(s):s for s in expected}; h=file_hash(config)
    rows=[];seen=set();counts={"duplicates":0,"corrupt":0,"identity_mismatches":0,"unexpected":0}
    for path in (root/"results/m10/development/runs").glob("*.json"):
        try: row=json.loads(path.read_text())
        except Exception: counts["corrupt"]+=1;continue
        rid=row.get("run_id")
        if rid in seen: counts["duplicates"]+=1;continue
        seen.add(rid)
        if rid not in expected_ids: counts["unexpected"]+=1;continue
        if row.get("config_hash")!=h or any(row.get(k)!=v for k,v in expected_ids[rid].items()):
            counts["identity_mismatches"]+=1;continue
        rows.append(row)
    missing=len(set(expected_ids)-{r["run_id"] for r in rows})
    report={"expected":len(expected),"unique_valid":len(rows),"missing":missing,**counts,"config_hash":h}
    report["complete"]=len(rows)==len(expected) and not any([missing,*counts.values()])
    return pd.DataFrame(rows),report


def m9_endpoints(root, cfg):
    rows=[]; seeds=set(cfg["development_seeds"]); envs=set(cfg["development_environment_ids"])
    profiles={f"{h}__{l}" for h,l in cfg["profiles"]}
    for path in (root/cfg["m9_endpoint_results"]).glob("*.json"):
        row=json.loads(path.read_text())
        if row.get("seed") in seeds and row.get("environment_id") in envs and row.get("alpha") in [0.,1.] and f"{row.get('learner_high')}__{row.get('learner_low')}" in profiles:
            rows.append(row)
    expected=2*len(seeds)*len(envs)*len(profiles)
    if len(rows)!=expected: raise RuntimeError(f"M9 endpoint mismatch: {len(rows)} != {expected}")
    return pd.DataFrame(rows)


def cvar(x,share=.1):
    x=np.sort(np.asarray(x,float));return float(x[-max(1,int(np.ceil(len(x)*share))):].mean())


def analyze(root,config):
    rows,integrity=validate(root,config)
    if not integrity["complete"]: raise RuntimeError(integrity)
    cfg=json.loads(config.read_text()); endpoints=m9_endpoints(root,cfg)
    keys=["learner_high","learner_low","environment_id","v_low","horizon","c_high","c_low"]
    ep=endpoints.groupby(keys,as_index=False)[["revenue","high_win","welfare"]].max().rename(columns={"revenue":"best_revenue","high_win":"best_allocation","welfare":"best_welfare"})
    cells=rows.groupby(["a","tau",*keys],as_index=False)[["revenue","high_win","welfare","bidder_surplus","normalized_gap","realized_alpha"]].mean().merge(ep,on=keys,validate="many_to_one")
    cells["q_revenue"]=(cells.best_revenue-cells.revenue)/cells.v_low.clip(lower=cfg["revenue_normalizer_floor"])
    cells["q_allocation"]=cells.best_allocation-cells.high_win;cells["q_welfare"]=cells.best_welfare-cells.welfare
    cells["q_joint"]=cells[["q_revenue","q_allocation"]].max(axis=1)
    records=[]
    for (a,tau),g in cells.groupby(["a","tau"]):
        r={"a":a,"tau":tau}
        for name in ["q_revenue","q_allocation","q_welfare","q_joint"]:
            x=g[name];r.update({f"{name}_mean":x.mean(),f"{name}_median":x.median(),f"{name}_p90":x.quantile(.9),f"{name}_p95":x.quantile(.95),f"{name}_worst":x.max(),f"{name}_cvar90":cvar(x)})
        r.update({"mean_gap":g.normalized_gap.mean(),"mean_realized_alpha":g.realized_alpha.mean()});records.append(r)
    frontier=pd.DataFrame(records)
    lim=cfg["eligibility"];eligible=frontier[(frontier.q_revenue_worst<=lim["worst_normalized_revenue_regret"])&(frontier.q_allocation_worst<=lim["worst_allocation_regret"])].copy()
    candidate=None
    if not eligible.empty:
        tol=cfg["metric_tie_tolerance"]
        for col in ["q_joint_worst","q_revenue_worst","q_allocation_worst"]: eligible[col+"_tie"]=(eligible[col]/tol).round()
        candidate=eligible.sort_values(["q_joint_worst_tie","q_revenue_worst_tie","q_allocation_worst_tie","tau","a"],ascending=[True,True,True,False,True]).iloc[0].to_dict()
    miss=cfg["refinement_floor_miss_tolerance"]
    near=frontier[(frontier.q_revenue_worst<=lim["worst_normalized_revenue_regret"]+miss)&(frontier.q_allocation_worst<=lim["worst_allocation_regret"]+miss)]
    refinement_triggered=candidate is not None or not near.empty
    strata=cells.groupby(["a","tau","v_low"],as_index=False)[["normalized_gap","realized_alpha","q_joint"]].mean()
    stress=cells[cells.v_low>=.7].groupby(["a","tau"],as_index=False).agg(high_v_mean_joint=("q_joint","mean"),high_v_worst_joint=("q_joint","max"))
    role=role_sensitivity(cells)
    out=root/"results/m10/development/analysis";fig=out/"figures";fig.mkdir(parents=True,exist_ok=True)
    cells.to_csv(out/"cell_metrics.csv",index=False);frontier.to_csv(out/"coarse_frontier.csv",index=False);strata.to_csv(out/"gap_diagnostics.csv",index=False);stress.to_csv(out/"high_v_stress.csv",index=False);role.to_csv(out/"role_sensitivity.csv",index=False)
    summary={"integrity":integrity,"candidate":candidate,"eligible_count":len(eligible),"near_count":len(near),"refinement_triggered":refinement_triggered}
    _atomic_json(out/"summary.json",summary);figures(frontier,strata,fig);return summary


def role_sensitivity(cells):
    out=[]
    for x,y in [("hedge","ftpl"),("hedge","regret_matching"),("ftpl","regret_matching")]:
        xy=cells[(cells.learner_high==x)&(cells.learner_low==y)];yx=cells[(cells.learner_high==y)&(cells.learner_low==x)]
        m=xy.merge(yx,on=["a","tau","environment_id"],suffixes=("_xy","_yx"))
        for (a,tau),g in m.groupby(["a","tau"]):
            sr=(g.revenue_xy-g.revenue_yx).abs();sa=(g.high_win_xy-g.high_win_yx).abs()
            out.append({"pair":f"{x}/{y}","a":a,"tau":tau,"S_R_median":sr.median(),"S_R_p95":sr.quantile(.95),"S_A_median":sa.median(),"S_A_p95":sa.quantile(.95)})
    return pd.DataFrame(out)


def figures(frontier,strata,out):
    p=frontier.pivot(index="a",columns="tau",values="q_joint_worst");plt.figure(figsize=(7,5));plt.imshow(p,aspect="auto",origin="lower");plt.xticks(range(len(p.columns)),p.columns);plt.yticks(range(len(p.index)),p.index);plt.xlabel("tau");plt.ylabel("a");plt.colorbar(label="Worst joint regret");plt.tight_layout();plt.savefig(out/"M10-F1_coarse_heatmap.png",dpi=180);plt.close()
    for metric,name in [("normalized_gap","gap"),("realized_alpha","alpha")]:
        plt.figure(figsize=(7,5))
        for (a,tau),g in strata.groupby(["a","tau"]): plt.plot(g.v_low,g[metric],alpha=.6,label=f"{a:g},{tau:g}")
        plt.xlabel("v_L");plt.ylabel(f"Mean {metric.replace('_',' ')}");plt.tight_layout();plt.savefig(out/f"M10-F2_{name}_by_valuation.png",dpi=180);plt.close()

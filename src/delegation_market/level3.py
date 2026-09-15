"""Frozen Level 3 FPA/SPA finite-horizon discovery runner."""
from __future__ import annotations
import argparse, hashlib, json, math, platform, time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from .agents import HedgeAgent
from .diagnostics import total_variation, wasserstein_1_ordered
from .mechanisms import run_auction
from .simulation import counterfactual_rewards


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_seed(mechanism, v_low, horizon, c_high, c_low, seed, step=.01, tail_share=.10):
    grids=[np.round(np.arange(0,1+step/2,step),10),np.round(np.arange(0,v_low+step/2,step),10)]
    etas=[c_high*math.sqrt(math.log(len(grids[0]))/horizon),c_low*math.sqrt(math.log(len(grids[1]))/horizon)]
    agents=[HedgeAgent(1,grids[0],etas[0],2*seed),HedgeAgent(v_low,grids[1],etas[1],2*seed+1)]
    rng=np.random.default_rng(seed+10_000); values=np.array([1.,v_low]); tail_start=int((1-tail_share)*horizon)
    sums={p+q:0. for p in ("full_","tail_") for q in ("revenue","welfare","high_win","surplus_high","surplus_low")}
    tail_n=horizon-tail_start; prior=None; start=time.perf_counter()
    for t in range(horizon):
        if t==tail_start: prior=[a.policy().copy() for a in agents]
        bids=np.array([a.act() for a in agents]); result=run_auction(bids,mechanism,rng=rng); rewards=result.allocations*values-result.payments
        for i,a in enumerate(agents): a.update(bids[i],rewards[i],counterfactual_rewards(a,i,bids,mechanism,0,1))
        vals={"revenue":float(result.payments.sum()),"welfare":float(result.allocations@values),"high_win":float(result.allocations[0]),"surplus_high":float(rewards[0]),"surplus_low":float(rewards[1])}
        for q,x in vals.items(): sums["full_"+q]+=x
        if t>=tail_start:
            for q,x in vals.items(): sums["tail_"+q]+=x
    terminal=[a.policy() for a in agents]; prior=prior or terminal
    row={"mechanism":mechanism,"v_high":1.,"v_low":v_low,"horizon":horizon,"learner":"Hedge","c_high":c_high,"c_low":c_low,"eta_high":etas[0],"eta_low":etas[1],"step":step,"seed":seed,"reference_revenue":v_low,"tail_share":tail_share}
    for q in ("revenue","welfare","high_win","surplus_high","surplus_low"):
        row["full_"+q]=sums["full_"+q]/horizon; row["tail_"+q]=sums["tail_"+q]/tail_n
    for prefix in ("full","tail"):
        row[prefix+"_dl_revenue"]=v_low-row[prefix+"_revenue"]; row[prefix+"_ndl_revenue"]=(v_low-row[prefix+"_revenue"])/v_low
        row[prefix+"_dl_ae"]=1-row[prefix+"_high_win"]; row[prefix+"_dl_welfare"]=1-row[prefix+"_welfare"]
        row[prefix+"_surplus_total"]=row[prefix+"_surplus_high"]+row[prefix+"_surplus_low"]
    for i,label in enumerate(("high","low")):
        p=terminal[i]; row["terminal_expected_bid_"+label]=float(p@grids[i]); row["terminal_entropy_"+label]=float(-(p*np.log(p+1e-300)).sum())
        row["terminal_truth_mass_"+label]=float(p[-1]); row["tail_policy_tv_"+label]=total_variation(prior[i],p); row["tail_policy_w1_"+label]=wasserstein_1_ordered(prior[i],p,grids[i])
        row["regret_per_round_"+label]=agents[i].diagnostics()["external_regret"]/horizon
    row["runtime_seconds"]=time.perf_counter()-start
    return row


def _task(x): return run_seed(*x)


def execute(root:Path, grid_path:Path, protocol_hash:str, git_commit:str, workers=12):
    grid=json.loads(grid_path.read_text(encoding="utf-8")); seeds=range(grid["seeds"]["start"],grid["seeds"]["start"]+grid["seeds"]["count"])
    tasks=[]
    for mechanism in grid["mechanisms"]:
      for vl in grid["v_low"]:
       for h in grid["horizons"]:
        for ch,cl in grid["rate_factors"]:
         for seed in seeds: tasks.append((mechanism,vl,h,ch,cl,seed,grid["bid_step"],grid["tail_share"]))
    started=time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool: rows=list(pool.map(_task,tasks,chunksize=1))
    frame=pd.DataFrame(rows); frame.insert(0,"experiment_id",grid["name"]); frame.insert(1,"protocol_hash",protocol_hash); frame.insert(2,"git_commit",git_commit)
    kind="development" if "DEVELOPMENT" in grid["name"] else "holdout"; out=root/"results"/"level_03"/kind; out.mkdir(parents=True,exist_ok=True); frame.to_csv(out/"seed_results.csv",index=False)
    runtime=time.perf_counter()-started; manifest={"experiment_id":grid["name"],"protocol_hash":protocol_hash,"grid_hash":file_hash(grid_path),"git_commit":git_commit,"timestamp":datetime.now(timezone.utc).isoformat(),"conditions":len(tasks),"seeds_per_condition":grid["seeds"]["count"],"logical_rounds":int(sum(x[2] for x in tasks)),"runtime_seconds":runtime,"workers":workers,"python":platform.python_version(),"result_path":str(out/"seed_results.csv")}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8"); print(json.dumps(manifest,indent=2))


def main():
    p=argparse.ArgumentParser(); p.add_argument("--grid",type=Path,required=True); p.add_argument("--protocol-hash",required=True); p.add_argument("--git-commit",required=True); p.add_argument("--workers",type=int,default=12); p.add_argument("--root",type=Path); a=p.parse_args()
    execute(a.root or Path(__file__).resolve().parents[2],a.grid,a.protocol_hash,a.git_commit,a.workers)
if __name__=="__main__": main()

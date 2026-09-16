"""Frozen Level 3 FPA/SPA finite-horizon discovery runner."""
from __future__ import annotations
import argparse, hashlib, json, math, os, platform, time
from concurrent.futures import FIRST_COMPLETED, BrokenExecutor, ProcessPoolExecutor, wait
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


def _atomic_json(path: Path, value) -> None:
    """Durably replace a JSON file without exposing a partial write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_name(path.name+f".tmp-{os.getpid()}")
    with temporary.open("w",encoding="utf-8",newline="\n") as handle:
        json.dump(value,handle,indent=2,sort_keys=True)
        handle.write("\n"); handle.flush(); os.fsync(handle.fileno())
    os.replace(temporary,path)


def _pair_id(v_low,horizon,c_high,c_low,step,tail_share,seed):
    key=json.dumps([v_low,horizon,c_high,c_low,step,tail_share,seed],separators=(",",":"))
    return "pair-"+hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]


def _paired_task(task):
    pair_id,args=task
    rows=[run_seed(mechanism,*args) for mechanism in ("first_price","second_price")]
    return {"pair_id":pair_id,"pair_seed":args[4],"rows":rows}


def _holdout_pairs(grid):
    seeds=range(grid["seeds"]["start"],grid["seeds"]["start"]+grid["seeds"]["count"])
    pairs=[]
    for vl in grid["v_low"]:
      for horizon in grid["horizons"]:
       for c_high,c_low in grid["rate_factors"]:
        for seed in seeds:
         pair_id=_pair_id(vl,horizon,c_high,c_low,grid["bid_step"],grid["tail_share"],seed)
         pairs.append((pair_id,(vl,horizon,c_high,c_low,seed,grid["bid_step"],grid["tail_share"])))
    return pairs


def _load_completed_pair(path,expected_id):
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError): return None
    if value.get("pair_id")!=expected_id or value.get("pair_seed") is None: return None
    rows=value.get("rows",[])
    if len(rows)!=2 or {r.get("mechanism") for r in rows}!={"first_price","second_price"}: return None
    return value


def execute_holdout_resumable(root:Path,grid_path:Path,protocol_hash:str,git_commit:str,workers=2,shard_index=0,shard_count=1,max_pairs=None,max_pool_restarts=20):
    """Execute the frozen holdout as durable, idempotent paired units."""
    if workers<1 or shard_count<1 or not 0<=shard_index<shard_count: raise ValueError("invalid workers or shard selection")
    grid=json.loads(grid_path.read_text(encoding="utf-8"))
    if grid.get("name")!="L3_HOLDOUT": raise ValueError("resumable runner is restricted to the frozen L3_HOLDOUT grid")
    all_pairs=_holdout_pairs(grid); expected_ids=[p[0] for p in all_pairs]
    if len(expected_ids)!=len(set(expected_ids)): raise ValueError("pair ID collision")
    selected=[p for i,p in enumerate(all_pairs) if i%shard_count==shard_index]
    out=root/"results"/"level_03"/"holdout"; parts=out/"pairs"; parts.mkdir(parents=True,exist_ok=True)
    completed={pid for pid,_ in all_pairs if _load_completed_pair(parts/f"{pid}.json",pid) is not None}
    pending=[p for p in selected if p[0] not in completed]
    if max_pairs is not None: pending=pending[:max_pairs]
    started=time.perf_counter(); restarts=0; failures=[]
    def checkpoint(status):
        manifest={"experiment_id":grid["name"],"status":status,"protocol_hash":protocol_hash,"grid_hash":file_hash(grid_path),"git_commit":git_commit,"timestamp":datetime.now(timezone.utc).isoformat(),"expected_pairs":len(all_pairs),"completed_pairs":len(completed),"remaining_pairs":len(all_pairs)-len(completed),"shard_index":shard_index,"shard_count":shard_count,"workers":workers,"pool_restarts":restarts,"failures":failures[-20:],"pair_id_set_hash":hashlib.sha256("\n".join(sorted(expected_ids)).encode()).hexdigest(),"parts_path":str(parts),"python":platform.python_version()}
        _atomic_json(out/"checkpoint.json",manifest); return manifest
    checkpoint("running")
    while pending:
        batch=pending; pending=[]
        try:
            with ProcessPoolExecutor(max_workers=workers) as pool:
                active={}; iterator=iter(batch)
                for _ in range(min(workers,len(batch))):
                    task=next(iterator); active[pool.submit(_paired_task,task)]=task
                while active:
                    done,_=wait(active,return_when=FIRST_COMPLETED)
                    for future in done:
                        task=active.pop(future); value=future.result()
                        _atomic_json(parts/f"{value['pair_id']}.json",value); completed.add(value["pair_id"]); checkpoint("running")
                        try: nxt=next(iterator)
                        except StopIteration: continue
                        active[pool.submit(_paired_task,nxt)]=nxt
        except BrokenExecutor as exc:
            restarts+=1; failures.append({"timestamp":datetime.now(timezone.utc).isoformat(),"type":type(exc).__name__,"message":str(exc)})
            checkpoint("recovering")
            pending=[p for p in batch if p[0] not in completed]
            if restarts>max_pool_restarts: raise RuntimeError("pool restart limit exceeded; completed pairs remain durable") from exc
    manifest=checkpoint("complete" if len(completed)==len(all_pairs) else "shard_complete")
    if len(completed)==len(all_pairs):
        values=[_load_completed_pair(parts/f"{pid}.json",pid) for pid in expected_ids]
        rows=[dict(row,pair_id=value["pair_id"]) for value in values for row in value["rows"]]
        frame=pd.DataFrame(rows); frame.insert(0,"experiment_id",grid["name"]); frame.insert(1,"protocol_hash",protocol_hash); frame.insert(2,"git_commit",git_commit)
        temporary=out/"seed_results.csv.tmp"; frame.to_csv(temporary,index=False); os.replace(temporary,out/"seed_results.csv")
        manifest.update({"conditions":len(frame),"logical_rounds":int(frame.horizon.sum()),"runtime_seconds_this_invocation":time.perf_counter()-started,"result_path":str(out/"seed_results.csv")})
        _atomic_json(out/"manifest.json",manifest)
    print(json.dumps(manifest,indent=2,sort_keys=True)); return manifest


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


def execute_falsification(root:Path, grid_path:Path, protocol_hash:str, git_commit:str, workers=12):
    grid=json.loads(grid_path.read_text(encoding="utf-8")); seeds=range(grid["seeds"]["start"],grid["seeds"]["start"]+grid["seeds"]["count"]); tasks=[]; labels=[]
    for case in grid["cases"]:
      for mechanism in grid["mechanisms"]:
       for seed in seeds:
        tasks.append((mechanism,case["v_low"],case["horizon"],case["c_high"],case["c_low"],seed,case["step"],case["tail_share"])); labels.append(case["case"])
    started=time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool: rows=list(pool.map(_task,tasks,chunksize=1))
    for row,label in zip(rows,labels): row["falsification_case"]=label
    frame=pd.DataFrame(rows); frame.insert(0,"experiment_id",grid["name"]); frame.insert(1,"protocol_hash",protocol_hash); frame.insert(2,"git_commit",git_commit)
    out=root/"results"/"level_03"/"falsification"; out.mkdir(parents=True,exist_ok=True); frame.to_csv(out/"seed_results.csv",index=False); runtime=time.perf_counter()-started
    manifest={"experiment_id":grid["name"],"protocol_hash":protocol_hash,"grid_hash":file_hash(grid_path),"git_commit":git_commit,"timestamp":datetime.now(timezone.utc).isoformat(),"conditions":len(tasks),"seeds_per_case":grid["seeds"]["count"],"logical_rounds":int(sum(x[2] for x in tasks)),"runtime_seconds":runtime,"workers":workers,"python":platform.python_version(),"result_path":str(out/"seed_results.csv")}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8"); print(json.dumps(manifest,indent=2))


def main():
    p=argparse.ArgumentParser(); p.add_argument("--grid",type=Path,required=True); p.add_argument("--protocol-hash",required=True); p.add_argument("--git-commit",required=True); p.add_argument("--workers",type=int,default=12); p.add_argument("--root",type=Path); p.add_argument("--falsification",action="store_true"); p.add_argument("--resumable-holdout",action="store_true"); p.add_argument("--shard-index",type=int,default=0); p.add_argument("--shard-count",type=int,default=1); p.add_argument("--max-pairs",type=int); a=p.parse_args(); root=a.root or Path(__file__).resolve().parents[2]
    if a.resumable_holdout: execute_holdout_resumable(root,a.grid,a.protocol_hash,a.git_commit,a.workers,a.shard_index,a.shard_count,a.max_pairs)
    else: (execute_falsification if a.falsification else execute)(root,a.grid,a.protocol_hash,a.git_commit,a.workers)
if __name__=="__main__": main()

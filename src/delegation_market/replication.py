import argparse, hashlib, json, math, platform, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from .agents import HedgeAgent
from .diagnostics import classify_convergence,total_variation,wasserstein_1_ordered
from .mechanisms import run_auction
from .simulation import counterfactual_rewards


def _hash(payload): return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",", ":")).encode()).hexdigest()


def run_hedge_seed(mechanism,seed,horizon=50_000,runner_ratio=1.0,step=.01,rate_schedule="ratio"):
    grids=[np.round(np.arange(0,1+step/2,step),10),np.round(np.arange(0,.5+step/2,step),10)]
    eta_high=math.sqrt(math.log(len(grids[0]))/horizon)
    eta_low=(math.sqrt(math.log(len(grids[1])))*horizon**(-1/3)) if rate_schedule=="diverging" else runner_ratio*math.sqrt(math.log(len(grids[1]))/horizon)
    rates=[eta_high,eta_low]
    agents=[HedgeAgent(1,grids[0],eta=rates[0],seed=2*seed),HedgeAgent(.5,grids[1],eta=rates[1],seed=2*seed+1)]
    rng=np.random.default_rng(seed+10_000); bids=np.empty((horizon,2)); prices=np.empty(horizon); wins=np.empty((horizon,2)); utility=np.empty((horizon,2))
    started=time.perf_counter(); prior_policies=None
    for t in range(horizon):
        if t==horizon-5_000: prior_policies=[a.policy().copy() for a in agents]
        action=np.array([a.act() for a in agents]); result=run_auction(action,mechanism,rng=rng); reward=result.allocations*np.array([1,.5])-result.payments
        for i,a in enumerate(agents): a.update(action[i],reward[i],counterfactual_rewards(a,i,action,mechanism,0,1))
        bids[t]=action; prices[t]=result.price; wins[t]=result.allocations; utility[t]=reward
    tail=slice(horizon//2,None); window=5_000
    diagnostics=[classify_convergence(bids[:,i],grids[i],window=window) for i in range(2)]
    terminal=[a.policy() for a in agents]; prior_policies=prior_policies or terminal
    return {
        "seed":seed,"mechanism":mechanism,"horizon":horizon,"runner_ratio":runner_ratio,"eta_high":rates[0],"eta_low":rates[1],
        "tail_mean_price":float(prices[tail].mean()),"tail_high_win_share":float(wins[tail,0].mean()),
        "first_half_mean_price":float(prices[:horizon//2].mean()),"first_half_high_win_share":float(wins[:horizon//2,0].mean()),
        "tail_mean_bid_high":float(bids[tail,0].mean()),"tail_mean_bid_low":float(bids[tail,1].mean()),
        "tail_utility_high":float(utility[tail,0].mean()),"tail_utility_low":float(utility[tail,1].mean()),
        "regret_per_round_high":agents[0].diagnostics()["external_regret"]/horizon,
        "regret_per_round_low":agents[1].diagnostics()["external_regret"]/horizon,
        "stability_high":diagnostics[0]["label"],"stability_low":diagnostics[1]["label"],
        "policy_l1_high":diagnostics[0]["policy_l1"],"policy_l1_low":diagnostics[1]["policy_l1"],
        "mean_drift_high":diagnostics[0]["mean_drift"],"mean_drift_low":diagnostics[1]["mean_drift"],
        "terminal_expected_bid_high":float(np.dot(terminal[0],grids[0])),"terminal_expected_bid_low":float(np.dot(terminal[1],grids[1])),
        "terminal_truth_tv_low":float(1-terminal[1][-1]),"terminal_truth_mass_low":float(terminal[1][-1]),
        "exact_policy_tv_5000_high":total_variation(prior_policies[0],terminal[0]),"exact_policy_tv_5000_low":total_variation(prior_policies[1],terminal[1]),
        "exact_policy_w1_5000_high":wasserstein_1_ordered(prior_policies[0],terminal[0],grids[0]),"exact_policy_w1_5000_low":wasserstein_1_ordered(prior_policies[1],terminal[1],grids[1]),
        "rate_schedule":rate_schedule,"rate_ratio":eta_low/eta_high,
        "runtime_seconds":time.perf_counter()-started,
    }


def execute(root,seeds=30,horizon=50_000):
    cases=[("R-REP-001","second_price",1.0),("R-REP-002","first_price",1.0),("R-REP-003-fast","second_price",10.0)]
    rows=[]; out=root/"results"/"replication"; out.mkdir(parents=True,exist_ok=True)
    for experiment_id,mechanism,ratio in cases:
        config={"experiment_id":experiment_id,"mechanism":mechanism,"values":[1,.5],"step":.01,"horizon":horizon,"runner_ratio":ratio,"seeds":list(range(seeds)),"feedback":"full_expected_counterfactual","overbidding":False}
        config_hash=_hash(config)
        for seed in range(seeds):
            result=run_hedge_seed(mechanism,seed,horizon,ratio); result.update({"experiment_id":experiment_id,"config_hash":config_hash}); rows.append(result)
        metadata={"timestamp":datetime.now(timezone.utc).isoformat(),"git_commit":None,"code_version":"0.2.0-phase2","config_hash":config_hash,"config":config,"result_path":str(out/"seed_results.csv"),"python":platform.python_version()}
        (out/f"{experiment_id}_manifest.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    df=pd.DataFrame(rows); df.to_csv(out/"seed_results.csv",index=False)
    numeric=df.select_dtypes(include="number").columns.difference(["seed"]); aggregate=df.groupby("experiment_id")[numeric].agg(["mean","std","median"]); aggregate.to_csv(out/"aggregate.csv")
    return df


def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path); p.add_argument("--seeds",type=int,default=30); p.add_argument("--horizon",type=int,default=50_000); a=p.parse_args()
    root=a.root or Path(__file__).resolve().parents[2]; df=execute(root,a.seeds,a.horizon); print(df.groupby("experiment_id")[["tail_mean_price","tail_high_win_share","tail_mean_bid_low","regret_per_round_high","regret_per_round_low"]].agg(["mean","std","median"]))


if __name__=="__main__": main()

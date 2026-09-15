import argparse,hashlib,json,platform,time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .replication import run_hedge_seed


def _task(args):
    target,schedule,horizon,seed=args
    return {"target":target,"schedule":schedule,**run_hedge_seed("first_price" if target=="R-REP-002-V2" else "second_price",seed,horizon=horizon,rate_schedule=schedule)}


def execute(root,protocol_hash,seeds=30,workers=4):
    tasks=[("R-REP-002-V2","ratio",50_000,s) for s in range(seeds)]
    for horizon in [25_000,50_000,100_000,200_000]:
        for schedule in ["ratio","diverging"]: tasks.extend(("R-REP-003-V2",schedule,horizon,s) for s in range(seeds))
    started=time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as pool: rows=list(pool.map(_task,tasks))
    out=root/"results"/"replication_v2"; out.mkdir(parents=True,exist_ok=True); df=pd.DataFrame(rows); df["protocol_version"]="v2"; df["protocol_hash"]=protocol_hash
    df.to_csv(out/"seed_results_v2.csv",index=False)
    aggregate=df.groupby(["target","schedule","horizon"])[df.select_dtypes("number").columns.difference(["seed","horizon"])].agg(["mean","std","median"]); aggregate.to_csv(out/"aggregate_v2.csv")
    commit=None
    metadata={"experiment_id":"LEVEL2-REPAIR-V2","protocol_version":"v2","protocol_hash":protocol_hash,"git_commit":commit,"timestamp":datetime.now(timezone.utc).isoformat(),"seeds":seeds,"horizons":[25000,50000,100000,200000],"rate_schedules":{"equal":"sqrt(log(K_i)/T)","diverging_runner":"eta_W=sqrt(log(K_W)/T); eta_R=sqrt(log(K_R))*T^(-1/3)"},"stability_metrics":["exact_policy_TV","Wasserstein-1","expected_bid_drift"],"result_path":str(out/"seed_results_v2.csv"),"runtime_seconds":time.perf_counter()-started,"python":platform.python_version()}
    (out/"manifest_v2.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    make_figures(df,out); return df,metadata


def make_figures(df,out):
    fpa=df[df.target=="R-REP-002-V2"].sort_values("seed")
    fig,ax=plt.subplots(2,2,figsize=(10,7)); ax=ax.ravel()
    ax[0].plot(fpa.seed,fpa.first_half_mean_price,label="first half"); ax[0].plot(fpa.seed,fpa.tail_mean_price,label="second half"); ax[0].axhline(.5,color="black",ls="--",lw=1); ax[0].set(xlabel="Seed",ylabel="Mean price",title="FPA price stability"); ax[0].legend()
    ax[1].scatter(fpa.exact_policy_tv_5000_high,fpa.policy_l1_high,s=18); ax[1].set(xlabel="Exact-policy TV, final 5,000 rounds",ylabel="Empirical marginal L1",title="Exact policy vs sampled histogram")
    ax[2].scatter(fpa.exact_policy_w1_5000_high,fpa.mean_drift_high,s=18); ax[2].set(xlabel="Exact-policy Wasserstein-1",ylabel="Empirical mean-bid drift",title="Geometry-aware stability")
    ax[3].plot(fpa.seed,fpa.tail_high_win_share); ax[3].axhline(.98,color="black",ls="--",lw=1); ax[3].set(xlabel="Seed",ylabel="High bidder win share",title="FPA allocation")
    fig.tight_layout(); fig.savefig(out/"r_rep_002_diagnostics.png",dpi=220); plt.close(fig)
    rate=df[df.target=="R-REP-003-V2"]; summary=rate.groupby(["schedule","horizon"]).agg(mean_bid=("terminal_expected_bid_low","mean"),se_bid=("terminal_expected_bid_low",lambda x:x.std(ddof=1)/np.sqrt(len(x))),mean_tv=("terminal_truth_tv_low","mean"),se_tv=("terminal_truth_tv_low",lambda x:x.std(ddof=1)/np.sqrt(len(x)))).reset_index()
    fig,ax=plt.subplots(1,2,figsize=(10,4))
    for schedule,g in summary.groupby("schedule"):
        ax[0].errorbar(g.horizon,g.mean_bid,yerr=1.96*g.se_bid,marker="o",label=schedule); ax[1].errorbar(g.horizon,g.mean_tv,yerr=1.96*g.se_tv,marker="o",label=schedule)
    ax[0].axhline(.5,color="black",ls="--",lw=1); ax[0].set(xscale="log",xlabel="Horizon",ylabel="Terminal expected runner bid",title="Last-iterate expected bid")
    ax[1].set(xscale="log",xlabel="Horizon",ylabel="TV distance to truthful point mass",title="Exact last-iterate truthfulness distance")
    for a in ax:a.legend()
    fig.tight_layout(); fig.savefig(out/"r_rep_003_horizon_ladder.png",dpi=220); plt.close(fig)


def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path); p.add_argument("--protocol-hash",required=True); p.add_argument("--seeds",type=int,default=30); p.add_argument("--workers",type=int,default=4); a=p.parse_args(); root=a.root or Path(__file__).resolve().parents[2]; df,m=execute(root,a.protocol_hash,a.seeds,a.workers); print(df.groupby(["target","schedule","horizon"])[["tail_mean_price","tail_high_win_share","terminal_expected_bid_low","terminal_truth_tv_low","exact_policy_tv_5000_high","exact_policy_tv_5000_low"]].agg(["mean","std","median"])); print(json.dumps(m,indent=2))


if __name__=="__main__":main()


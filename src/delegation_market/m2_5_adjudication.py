"""Descriptive M2.5 analysis of preserved V2 data; no new R-REP runs."""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import pandas as pd


def fit_line(x, y):
    return np.polyfit(x, y, 1)


def predict(model, coef, t):
    slope, intercept=coef
    if model=="power": return np.exp(intercept+slope*np.log(t))
    if model=="log": return intercept+slope*np.log(t)
    return intercept+slope/np.log(t)


def threshold_log10(model, coef, target):
    slope, intercept=coef
    try:
        if model=="power": logt=(math.log(target)-intercept)/slope
        elif model=="log": logt=(target-intercept)/slope
        else: logt=slope/(target-intercept)
        return logt/math.log(10) if logt >= 0 else None
    except (ValueError, ZeroDivisionError, OverflowError): return None


def main(root: Path):
    df=pd.read_csv(root/"results"/"replication_v2"/"seed_results_v2.csv")
    d=df[(df.target=="R-REP-003-V2") & (df.schedule=="diverging")]
    means=d.groupby("horizon").terminal_truth_tv_low.mean().sort_index()
    t=means.index.to_numpy(float); y=means.to_numpy(float)
    transforms={"power":(np.log(t),np.log(y)),"log":(np.log(t),y),"inverse_log":(1/np.log(t),y)}
    records=[]
    for model,(x,fy) in transforms.items():
        coef=fit_line(x,fy)
        residual=[]
        for i in range(len(t)):
            train=np.arange(len(t))!=i; c=fit_line(x[train],fy[train]); residual.append(predict(model,c,t[i])-y[i])
        rec={"model":model,"slope":float(coef[0]),"intercept":float(coef[1]),"loho_rmse":float(np.sqrt(np.mean(np.square(residual))))}
        for target in (.9,.75,.5,.25,.1): rec[f"tv_{target}_log10_horizon"]=threshold_log10(model,coef,target)
        records.append(rec)
    out=root/"results"/"m2_5_adjudication"; out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame({"horizon":t.astype(int),"mean_diverging_tv":y}).to_csv(out/"r_rep_003_observed_means.csv",index=False)
    pd.DataFrame(records).to_csv(out/"r_rep_003_descriptive_scaling.csv",index=False)
    kw,kr=101,51; coefficient=math.sqrt(math.log(kr)/math.log(kw)); throughput=24_000_000/796.2551618000143
    ratio=[]
    for q in (8,10,15,20,30):
        horizon=(q/coefficient)**6
        ratio.append({"rate_ratio":q,"horizon":horizon,"log10_horizon":math.log10(horizon),"one_schedule_30_seed_hours":30*horizon/throughput/3600,"paired_30_seed_hours":60*horizon/throughput/3600})
    pd.DataFrame(ratio).to_csv(out/"r_rep_003_rate_ratio_horizons.csv",index=False)
    meta={"label":"EMPIRICAL EXTRAPOLATION - NOT A THEORETICAL RESULT","rate_ratio_coefficient":coefficient,"observed_v2_throughput_rounds_per_second":throughput,"models":records}
    (out/"analysis_manifest.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(pd.DataFrame(ratio).to_string(index=False)); print(pd.DataFrame(records).to_string(index=False))


if __name__=="__main__": main(Path(__file__).resolve().parents[2])

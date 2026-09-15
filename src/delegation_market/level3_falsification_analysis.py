"""Evaluate the frozen Level 3 C3 falsification rules."""
from pathlib import Path
import json, math
import numpy as np
import pandas as pd


def ci(x):
    x=np.asarray(x,float); m=x.mean(); h=2.009*x.std(ddof=1)/math.sqrt(len(x)); return m,m-h,m+h


def main(root:Path):
    df=pd.read_csv(root/"results"/"level_03"/"falsification"/"seed_results.csv")
    keys=["falsification_case","v_low","horizon","c_high","c_low","step","tail_share","seed"]
    a=df[df.mechanism=="first_price"].set_index(keys); b=df[df.mechanism=="second_price"].set_index(keys); ix=a.index.intersection(b.index)
    p=pd.DataFrame(index=ix).reset_index()
    for m in ["full_ndl_revenue","full_dl_ae","full_dl_welfare","tail_ndl_revenue","tail_dl_ae","tail_dl_welfare"]: p["delta_"+m]=a.loc[ix,m].to_numpy()-b.loc[ix,m].to_numpy()
    rows=[]
    for case,g in p.groupby("falsification_case"):
        r={"case":case,"n":len(g)}
        use="tail" if case.startswith("tail_") else "full"
        for metric in ("ndl_revenue","dl_ae","dl_welfare"):
            m,lo,hi=ci(g[f"delta_{use}_{metric}"]); r["delta_"+metric]=m; r["ci_low_"+metric]=lo; r["ci_high_"+metric]=hi
        base_r=.5522283333333308 if use=="tail" else .6621526666667336; base_ae=.005733333333333335 if use=="tail" else .012983333333333312; base_w=.004586666666666533 if use=="tail" else .010386666666666907
        r["direction_survives"]=bool(r["delta_ndl_revenue"]<0 and (r["delta_dl_ae"]>0 or r["delta_dl_welfare"]>0))
        r["half_magnitude_survives"]=bool(abs(r["delta_ndl_revenue"])>=.5*base_r and (r["delta_dl_ae"]>=.5*base_ae or r["delta_dl_welfare"]>=.5*base_w))
        r["ci_survives"]=bool(r["ci_high_ndl_revenue"]<0 and (r["ci_low_dl_ae"]>0 or r["ci_low_dl_welfare"]>0))
        r["case_pass"]=bool(r["direction_survives"] and r["half_magnitude_survives"] and r["ci_survives"])
        if case=="independent_seeds": r["case_pass"]=bool(r["case_pass"] and abs(r["delta_ndl_revenue"])>=.05 and (r["delta_dl_ae"]>=.01 or r["delta_dl_welfare"]>=.005))
        rows.append(r)
    out=pd.DataFrame(rows).sort_values("case"); path=root/"results"/"level_03"/"falsification"/"summary.csv"; out.to_csv(path,index=False)
    verdict={"all_cases_pass":bool(out.case_pass.all()),"cases_passed":int(out.case_pass.sum()),"cases_total":len(out)}; (path.parent/"verdict.json").write_text(json.dumps(verdict,indent=2),encoding="utf-8"); print(out.to_string(index=False)); print(verdict)


if __name__=="__main__": main(Path(__file__).resolve().parents[2])

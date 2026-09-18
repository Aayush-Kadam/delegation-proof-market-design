"""Preregistered heterogeneous-learner analysis after the 9,000-run seal opened."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROFILES = ["hedge__ftpl", "ftpl__hedge", "hedge__regret_matching",
            "regret_matching__hedge", "ftpl__regret_matching", "regret_matching__ftpl"]
LABEL = {"hedge__ftpl": "H/F", "ftpl__hedge": "F/H", "hedge__regret_matching": "H/R",
         "regret_matching__hedge": "R/H", "ftpl__regret_matching": "F/R",
         "regret_matching__ftpl": "R/F"}


def normal_ci(x):
    x = np.asarray(x, float); mean = float(x.mean()); half = 1.96 * float(x.std(ddof=1)) / np.sqrt(len(x))
    return mean, mean - half, mean + half


def median_ci(x, seed):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    boot = np.median(rng.choice(x, size=(20000, len(x)), replace=True), axis=1)
    return [float(np.median(x)), *map(float, np.quantile(boot, [.025, .975]))]


def main(root: Path):
    out = root / "results/heterogeneous/analysis"; figs = out / "figures"; figs.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(p.read_text()) for p in (root / "results/heterogeneous/runs").glob("*.json")]
    df = pd.DataFrame(rows); assert len(df) == 9000 and df.run_id.nunique() == 9000
    idx = ["profile", "v_low", "horizon", "c_high", "c_low", "seed"]
    fpa = df[df.mechanism == "first_price"].set_index(idx).sort_index()
    spa = df[df.mechanism == "second_price"].set_index(idx).sort_index(); assert fpa.index.equals(spa.index)
    pairs = pd.DataFrame(index=fpa.index).reset_index()
    pairs["D_R"] = (fpa.revenue - spa.revenue).to_numpy()
    pairs["D_A"] = (spa.high_win - fpa.high_win).to_numpy()
    pairs["D_W"] = (spa.welfare - fpa.welfare).to_numpy(); pairs.to_csv(out / "paired_seed_gaps.csv", index=False)
    cell_keys = ["profile", "v_low", "horizon", "c_high", "c_low"]
    cell_rows = []
    for key, g in pairs.groupby(cell_keys, sort=True):
        r = normal_ci(g.D_R); a = normal_ci(g.D_A); w = normal_ci(g.D_W)
        profile, v, horizon, ch, cl = key
        cell_rows.append({"profile":profile,"v_low":v,"horizon":horizon,"c_high":ch,"c_low":cl,
                          "D_R":r[0],"D_R_ci_low":r[1],"D_R_ci_high":r[2],
                          "D_A":a[0],"D_A_ci_low":a[1],"D_A_ci_high":a[2],
                          "D_W":w[0],"D_W_ci_low":w[1],"D_W_ci_high":w[2],
                          "conflict_pass":bool(r[0]/v >= .05 and a[0] >= .01 and r[1] > 0 and a[1] > 0)})
    cells = pd.DataFrame(cell_rows); cells.to_csv(out / "cell_summary.csv", index=False)
    summaries = {}
    for j, profile in enumerate(PROFILES):
        c = cells[cells.profile == profile]; passed = int(c.conflict_pass.sum())
        mr, ma, mw = median_ci(c.D_R, 7101+j*10), median_ci(c.D_A, 7102+j*10), median_ci(c.D_W, 7103+j*10)
        if passed >= 15 and mr[0] > 0 and ma[0] > 0: classification = "STRONG ROBUSTNESS"
        elif passed >= 10 and mr[0] > 0 and ma[0] > 0: classification = "PARTIAL ROBUSTNESS"
        elif mr[0] > 0 and ma[0] > 0: classification = "DIRECTION-ONLY"
        else: classification = "REVERSAL / FAILURE"
        by_v = {str(v):{"passed":int(g.conflict_pass.sum()),"total":int(len(g)),"median_D_R":float(g.D_R.median()),"median_D_A":float(g.D_A.median()),"median_D_W":float(g.D_W.median())} for v,g in c.groupby("v_low")}
        by_h = {str(int(h)):{"passed":int(g.conflict_pass.sum()),"total":int(len(g)),"median_D_R":float(g.D_R.median()),"median_D_A":float(g.D_A.median()),"median_D_W":float(g.D_W.median())} for h,g in c.groupby("horizon")}
        d = df[df.profile == profile]
        regret = {m:{"high_mean":float(x.regret_high.mean()),"high_median":float(x.regret_high.median()),"low_mean":float(x.regret_low.mean()),"low_median":float(x.regret_low.median())} for m,x in d.groupby("mechanism")}
        summaries[profile] = {"label":LABEL[profile],"cells_passed":passed,"classification":classification,
                              "median_D_R_ci95":mr,"median_D_A_ci95":ma,"median_D_W_ci95":mw,
                              "by_valuation":by_v,"by_horizon":by_h,"regret":regret}

    role_specs = [("hedge__ftpl","ftpl__hedge","H/F minus F/H"),
                  ("hedge__regret_matching","regret_matching__hedge","H/R minus R/H"),
                  ("ftpl__regret_matching","regret_matching__ftpl","F/R minus R/F")]
    role = {}
    env = ["v_low","horizon","c_high","c_low"]
    for j,(a,b,name) in enumerate(role_specs):
        ca=cells[cells.profile==a].set_index(env).sort_index(); cb=cells[cells.profile==b].set_index(env).sort_index()
        gr=ca.D_R-cb.D_R; ga=ca.D_A-cb.D_A
        gate_change=(ca.conflict_pass != cb.conflict_pass)
        revenue_sign=(np.sign(ca.D_R) != np.sign(cb.D_R)); allocation_sign=(np.sign(ca.D_A) != np.sign(cb.D_A))
        role[name]={"median_Gamma_R_ci95":median_ci(gr,8101+j*10),"median_Gamma_A_ci95":median_ci(ga,8102+j*10),
                    "gate_change_fraction":float(gate_change.mean()),
                    "magnitude_only_change_fraction":float((gate_change & ~revenue_sign & ~allocation_sign).mean()),
                    "revenue_sign_swap_fraction":float(revenue_sign.mean()),"allocation_sign_swap_fraction":float(allocation_sign.mean())}

    sign_rows=[]
    for key,g in cells.groupby(env):
        pr=int((g.D_R>0).sum()); pa=int((g.D_A>0).sum())
        sign_rows.append({**dict(zip(env,key)),"positive_D_R_profiles":pr,"positive_D_A_profiles":pa,
                          "unanimous_joint":bool(pr==6 and pa==6),"majority_joint":bool(pr>=4 and pa>=4)})
    signs=pd.DataFrame(sign_rows); signs.to_csv(out / "cross_profile_signs.csv",index=False)
    reversals=cells[(cells.D_R<0)|(cells.D_A<0)].copy(); reversals.to_csv(out / "ranking_reversals.csv",index=False)
    stress=cells.assign(normalized_R=cells.D_R/cells.v_low, gate_margin=lambda x:np.minimum(x.normalized_R-.05,x.D_A-.01)).sort_values("gate_margin").head(20)
    stress.to_csv(out / "mechanism_design_stress_cells.csv",index=False)

    homogeneous=pd.read_csv(root/"results/level_05/analysis/cell_summary.csv")
    hom=[]
    for learner,g in homogeneous.groupby("learner"):
        hom.append({"profile":f"{learner}__{learner}","type":"homogeneous","cells_passed":int(g.conflict_pass.sum()),"median_D_R":float(g.D_R.median()),"median_D_A":float(g.D_A.median()),"median_D_W":float(g.D_W.median())})
    het=[{"profile":p,"type":"heterogeneous","cells_passed":s["cells_passed"],"median_D_R":s["median_D_R_ci95"][0],"median_D_A":s["median_D_A_ci95"][0],"median_D_W":s["median_D_W_ci95"][0]} for p,s in summaries.items()]
    combined=pd.DataFrame(hom+het); combined.to_csv(out/"homogeneous_heterogeneous_comparison.csv",index=False)
    strong=sum(s["classification"]=="STRONG ROBUSTNESS" for s in summaries.values())
    no_reversal=all(s["median_D_R_ci95"][0]>0 and s["median_D_A_ci95"][0]>0 for s in summaries.values())
    if strong>=5 and no_reversal: verdict="STRONG HETEROGENEOUS ROBUSTNESS"
    elif sum(s["classification"] in ["STRONG ROBUSTNESS","PARTIAL ROBUSTNESS"] for s in summaries.values())>=4 and no_reversal: verdict="HETEROGENEOUS ROBUSTNESS"
    elif no_reversal: verdict="MIXED — ROLE/LEARNER DEPENDENT"
    else: verdict="HETEROGENEOUS FAILURE"
    weakest={"gate_support":min(PROFILES,key=lambda p:summaries[p]["cells_passed"]),
             "median_D_R":min(PROFILES,key=lambda p:summaries[p]["median_D_R_ci95"][0]),
             "median_D_A":min(PROFILES,key=lambda p:summaries[p]["median_D_A_ci95"][0]),
             "median_D_W":min(PROFILES,key=lambda p:summaries[p]["median_D_W_ci95"][0])}
    result={"verdict":verdict,"profiles":summaries,"role_swaps":role,"sign_agreement":{"unanimous_joint_environments":int(signs.unanimous_joint.sum()),"majority_joint_environments":int(signs.majority_joint.sum()),"total":25,"reversal_cells":int(len(reversals))},"weakest":weakest,"falsification_required_by_frozen_protocol":False,"completeness":{"expected":9000,"unique":9000,"missing":0,"duplicates":0,"corrupt":0,"identity_mismatches":0}}
    (out/"summary.json").write_text(json.dumps(result,indent=2)+"\n")

    colors=["#3569a8","#e17c36","#4b9b63","#9067a8","#c44e52","#8172b3"]
    labels=[LABEL[p] for p in PROFILES]
    plt.figure(figsize=(8,4)); plt.bar(labels,[summaries[p]["cells_passed"] for p in PROFILES],color=colors); plt.axhline(15,color="black",ls="--",lw=1); plt.ylabel("Joint-gate cells (out of 25)"); plt.tight_layout(); plt.savefig(figs/"H1_gate_support.png",dpi=200); plt.close()
    for metric,name,ylabel in [("D_R","H2_revenue_gaps.png","D_R"),("D_A","H3_allocation_gaps.png","D_A")]:
        plt.figure(figsize=(8,4)); plt.boxplot([cells[cells.profile==p][metric] for p in PROFILES],tick_labels=labels); plt.axhline(0,color="black",lw=1); plt.ylabel(ylabel); plt.tight_layout(); plt.savefig(figs/name,dpi=200); plt.close()
    fig,ax=plt.subplots(figsize=(8,4)); x=np.arange(3); width=.35
    rvals=[role[n]["median_Gamma_R_ci95"][0] for _,_,n in role_specs]; avals=[role[n]["median_Gamma_A_ci95"][0] for _,_,n in role_specs]
    ax.bar(x-width/2,rvals,width,label="Gamma_R"); ax.bar(x+width/2,avals,width,label="Gamma_A"); ax.axhline(0,color="black",lw=1); ax.set_xticks(x,[n for _,_,n in role_specs]); ax.legend(); fig.tight_layout(); fig.savefig(figs/"H4_role_swap_effects.png",dpi=200); plt.close(fig)
    for col,name in [("v_low","H5_profile_valuation_heatmap.png"),("horizon","H6_profile_horizon_heatmap.png")]:
        heat=cells.pivot_table(index="profile",columns=col,values="conflict_pass",aggfunc="mean").loc[PROFILES]
        plt.figure(figsize=(8,4)); plt.imshow(heat,vmin=0,vmax=1,cmap="YlGn"); plt.xticks(range(len(heat.columns)),heat.columns); plt.yticks(range(6),labels); plt.colorbar(label="Gate-pass share"); plt.tight_layout(); plt.savefig(figs/name,dpi=200); plt.close()
    plt.figure(figsize=(10,4)); plt.bar(range(len(combined)),combined.cells_passed,color=["#888888" if x=="homogeneous" else "#3569a8" for x in combined.type]); plt.xticks(range(len(combined)),combined.profile,rotation=35,ha="right"); plt.ylabel("Gate cells (out of 25)"); plt.tight_layout(); plt.savefig(figs/"H7_homogeneous_vs_heterogeneous.png",dpi=200); plt.close()
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--root",type=Path,required=True); main(parser.parse_args().root)

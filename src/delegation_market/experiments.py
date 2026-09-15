import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from .agents import TruthfulAgent, HedgeAgent, Exp3Agent, QLearningAgent, UCBAgent
from .simulation import SimulationConfig, simulate


AGENTS={"truthful":TruthfulAgent,"hedge":HedgeAgent,"exp3":Exp3Agent,"q":QLearningAgent,"ucb":UCBAgent}


def build_agent(name,value,grid,seed): return AGENTS[name](value,grid,seed=seed)


def run_suite(root,quick=False):
    rounds=1_000 if quick else 10_000; seeds=range(3 if quick else 10); grid=np.linspace(0,1,101); summaries=[]
    raw=root/"results"/"raw"; processed=root/"results"/"processed"; tables=root/"results"/"tables"
    raw.mkdir(parents=True,exist_ok=True); processed.mkdir(parents=True,exist_ok=True); tables.mkdir(parents=True,exist_ok=True)
    for mechanism in ["first_price","second_price"]:
        for pair in [("truthful","truthful"),("hedge","hedge"),("exp3","exp3"),("q","q"),("q","truthful")]:
            for seed in seeds:
                agents=[build_agent(pair[0],1.0,grid,2*seed),build_agent(pair[1],.6,grid,2*seed+1)]
                cfg=SimulationConfig(mechanism=mechanism,rounds=rounds,seed=seed,record_every=max(1,rounds//1000))
                frame,metrics=simulate(agents,cfg); run_id=f"{mechanism}_{pair[0]}-{pair[1]}_s{seed}"
                frame.to_csv(raw/f"{run_id}.csv",index=False); summaries.append({"run_id":run_id,"mechanism":mechanism,"agents":"-".join(pair),"seed":seed,**metrics})
    df=pd.DataFrame(summaries); df.to_csv(processed/"smoke_summary.csv",index=False)
    numeric=[c for c in df.columns if c.startswith("mean_") or c in ["welfare_ratio","allocative_efficiency"]]
    df.groupby(["mechanism","agents"])[numeric].agg(["mean","std"]).to_csv(tables/"smoke_aggregate.csv")
    (processed/"manifest.json").write_text(json.dumps({"diagnostic_only":True,"rounds":rounds,"seeds":list(seeds),"bid_grid":"0:0.01:1"},indent=2))
    return df


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--quick",action="store_true"); parser.add_argument("--root",type=Path)
    args=parser.parse_args(); root=args.root or Path(__file__).resolve().parents[2]; df=run_suite(root,args.quick); print(df.to_string(index=False))


if __name__=="__main__": main()


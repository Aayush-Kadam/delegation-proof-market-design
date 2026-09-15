import json
from pathlib import Path
import numpy as np
from .diagnostics import stationary_null_l1


def run(root,repetitions=20_000,sample_size=5_000):
    results={"design":"prospective null; no R-REP-002 outcomes used to select policies or threshold","threshold_l1":.10,"sample_size":sample_size,"repetitions":repetitions,"policies":{}}
    for k in [51,101]:
        policies={"uniform":np.ones(k)/k,"smooth_triangular":np.arange(1,k+1,dtype=float)}; policies["smooth_triangular"]/=policies["smooth_triangular"].sum()
        for name,p in policies.items():
            d=stationary_null_l1(p,sample_size,repetitions,seed=20260915+k)
            results["policies"][f"{name}_K{k}"]={"mean":float(d.mean()),"q025":float(np.quantile(d,.025)),"q50":float(np.quantile(d,.5)),"q95":float(np.quantile(d,.95)),"q975":float(np.quantile(d,.975)),"false_rejection_rate":float((d>.10).mean())}
    out=root/"results"/"replication_v2"; out.mkdir(parents=True,exist_ok=True); (out/"v1_l1_null_diagnostic.json").write_text(json.dumps(results,indent=2),encoding="utf-8"); return results


if __name__=="__main__": print(json.dumps(run(Path(__file__).resolve().parents[2]),indent=2))

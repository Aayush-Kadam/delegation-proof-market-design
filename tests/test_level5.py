import json
from pathlib import Path
import numpy as np
from delegation_market.level5 import FTPLAgent,RegretMatchingAgent,job_id,tasks

def test_ftpl_and_rm_require_full_information():
    g=np.array([0.,.5,1.]);f=FTPLAgent(1,g,.1,1);r=RegretMatchingAgent(1,g,.1,2)
    for a in (f,r):
        x=a.act();a.update(x,0,np.array([0.,.2,.1]));assert abs(a.policy().sum()-1)<1e-12

def test_ids_deterministic_and_unique(tmp_path):
    cfg=json.loads((Path(__file__).parents[1]/'configs/level_05/environments.json').read_text());ts=tasks(cfg);ids=[job_id(x)for x in ts]
    assert len(ts)==4500 and len(ids)==len(set(ids))
    assert sum(x[3] for x in ts)==144_000_000

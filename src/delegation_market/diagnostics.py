import numpy as np


def policy_l1_distance(first_actions,second_actions,grid):
    """L1 distance between empirical action distributions in two windows."""
    edges=np.r_[grid-(grid[1]-grid[0])/2,grid[-1]+(grid[1]-grid[0])/2]
    p=np.histogram(first_actions,bins=edges)[0]; q=np.histogram(second_actions,bins=edges)[0]
    p=p/max(p.sum(),1); q=q/max(q.sum(),1); return float(np.abs(p-q).sum())


def classify_convergence(actions,grid,window=5000,l1_threshold=.10,mean_drift_threshold=.02):
    """Predeclared finite-horizon stability label, not asymptotic convergence."""
    a=np.asarray(actions,float)
    if len(a)<2*window: return {"label":"insufficient_horizon","policy_l1":float("nan"),"mean_drift":float("nan")}
    x,y=a[-2*window:-window],a[-window:]
    d=policy_l1_distance(x,y,np.asarray(grid)); drift=float(abs(x.mean()-y.mean()))
    label="stable_tail" if d<=l1_threshold and drift<=mean_drift_threshold else "unstable_tail"
    return {"label":label,"policy_l1":d,"mean_drift":drift}


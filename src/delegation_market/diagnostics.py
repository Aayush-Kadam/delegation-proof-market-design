import numpy as np


def policy_l1_distance(first_actions,second_actions,grid):
    """L1 distance between empirical action distributions in two windows."""
    edges=np.r_[grid-(grid[1]-grid[0])/2,grid[-1]+(grid[1]-grid[0])/2]
    p=np.histogram(first_actions,bins=edges)[0]; q=np.histogram(second_actions,bins=edges)[0]
    p=p/max(p.sum(),1); q=q/max(q.sum(),1); return float(np.abs(p-q).sum())


def total_variation(p,q):
    p=np.asarray(p,float); q=np.asarray(q,float)
    if p.shape!=q.shape or not np.isclose(p.sum(),1) or not np.isclose(q.sum(),1): raise ValueError("p and q must be same-shape probability vectors")
    return float(.5*np.abs(p-q).sum())


def wasserstein_1_ordered(p,q,grid):
    """Exact W1 for distributions supported on a shared ordered 1D grid."""
    p=np.asarray(p,float); q=np.asarray(q,float); x=np.asarray(grid,float)
    if p.shape!=q.shape or p.shape!=x.shape or np.any(np.diff(x)<0): raise ValueError("aligned ordered supports required")
    if not np.isclose(p.sum(),1) or not np.isclose(q.sum(),1): raise ValueError("probability vectors must sum to one")
    return float(np.sum(np.abs(np.cumsum(p-q)[:-1])*np.diff(x)))


def stationary_null_l1(policy,sample_size,repetitions=10_000,seed=20260915):
    """Null distribution from two samples drawn from one fixed policy."""
    p=np.asarray(policy,float); rng=np.random.default_rng(seed); out=np.empty(repetitions)
    for r in range(repetitions):
        a=rng.multinomial(sample_size,p)/sample_size; b=rng.multinomial(sample_size,p)/sample_size; out[r]=np.abs(a-b).sum()
    return out


def classify_convergence(actions,grid,window=5000,l1_threshold=.10,mean_drift_threshold=.02):
    """Predeclared finite-horizon stability label, not asymptotic convergence."""
    a=np.asarray(actions,float)
    if len(a)<2*window: return {"label":"insufficient_horizon","policy_l1":float("nan"),"mean_drift":float("nan")}
    x,y=a[-2*window:-window],a[-window:]
    d=policy_l1_distance(x,y,np.asarray(grid)); drift=float(abs(x.mean()-y.mean()))
    label="stable_tail" if d<=l1_threshold and drift<=mean_drift_threshold else "unstable_tail"
    return {"label":label,"policy_l1":d,"mean_drift":drift}

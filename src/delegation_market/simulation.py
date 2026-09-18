from dataclasses import dataclass, asdict
import hashlib, json
import numpy as np
import pandas as pd
from .mechanisms import run_auction
from .metrics import summarize


@dataclass(frozen=True)
class SimulationConfig:
    mechanism: str = "first_price"
    rounds: int = 10_000
    reserve: float = 0.0
    alpha: float = 1.0
    seed: int = 0
    record_every: int = 1


def counterfactual_rewards(agent, own_index, bids, mechanism, reserve, alpha, tau=1.0):
    """Expected utilities for each action against realized rival bids.

    Ties are evaluated in expectation under uniform tie-breaking; sampling them
    here would bias full-information learner updates.
    """
    grid=agent.bid_grid; others=np.delete(np.asarray(bids,float),own_index); top=float(others.max()) if others.size else 0.0
    tied=(others==grid[:,None]).sum(axis=1) if others.size else np.zeros(len(grid)); win=(grid>top).astype(float); tie=(grid==top)/(tied+1)
    alloc=np.where(grid>top,1.0,np.where(grid==top,tie,0.0)); alloc=np.where(grid>=reserve,alloc,0.0)
    if mechanism in {"first_price","reserve_first_price"}: utility=alloc*(agent.value-grid)
    elif mechanism in {"second_price","reserve_second_price"}: utility=alloc*(agent.value-np.maximum(reserve,top))
    elif mechanism=="hybrid": utility=alloc*(agent.value-np.maximum(reserve,alpha*grid+(1-alpha)*top))
    elif mechanism=="gap_adaptive":
        high=np.maximum(grid,top);second=np.minimum(grid,top);gap=np.divide(high-second,high,out=np.zeros_like(high),where=high>0)
        weight=alpha+(1-alpha)*np.minimum(gap/tau,1.0);payment=np.maximum(reserve,second+weight*(high-second));utility=alloc*(agent.value-payment)
    elif mechanism=="all_pay": utility=alloc*agent.value-grid
    else: raise ValueError(f"unknown mechanism: {mechanism}")
    return utility


def simulate(agents, config):
    if config.rounds <= 0 or config.record_every <= 0: raise ValueError("rounds and record_every must be positive")
    rng=np.random.default_rng(config.seed); rows=[]
    for t in range(config.rounds):
        bids=np.array([a.act() for a in agents]); values=np.array([a.value for a in agents])
        result=run_auction(bids, config.mechanism, config.reserve, config.alpha, rng)
        rewards=result.allocations*values-result.payments
        for i,a in enumerate(agents):
            rv=counterfactual_rewards(a,i,bids,config.mechanism,config.reserve,config.alpha) if a.__class__.__name__=="HedgeAgent" else None
            a.update(bids[i], rewards[i], rv)
        if t % config.record_every == 0:
            for i in range(len(agents)):
                rows.append({"round":t,"bidder":i,"value":values[i],"bid":bids[i],"allocated":result.allocations[i],"payment":result.payments[i],"utility":rewards[i],"price":result.price})
    frame=pd.DataFrame(rows)
    wide=lambda c: frame.pivot(index="round",columns="bidder",values=c).to_numpy()
    metrics=summarize(wide("value"),wide("bid"),wide("allocated"),wide("payment"))
    payload=json.dumps(asdict(config),sort_keys=True).encode(); metrics["config_sha256"]=hashlib.sha256(payload).hexdigest()
    return frame, metrics

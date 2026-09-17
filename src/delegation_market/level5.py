"""Crash-safe Level-5 cross-learner validation runner."""
from __future__ import annotations
import argparse,hashlib,json,math,os,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import numpy as np
from delegation_market.level3 import _atomic_json,file_hash
from delegation_market.mechanisms import run_auction
from delegation_market.simulation import counterfactual_rewards
from delegation_market.agents import HedgeAgent

class FTPLAgent:
 def __init__(self,value,grid,eta,seed):
  self.value=value;self.bid_grid=np.asarray(grid);self.eta=eta;self.rng=np.random.default_rng(seed);self.cum=np.zeros(len(grid));self.actual=0.;self.noise=self.rng.exponential(1/max(eta,1e-12),len(grid))
 def policy(self):
  z=self.cum+self.noise;m=z.max();idx=np.flatnonzero(z==m);p=np.zeros(len(z));p[idx]=1/len(idx);return p
 def act(self):return float(self.rng.choice(self.bid_grid,p=self.policy()))
 def update(self,a,r,reward_vector):self.cum+=reward_vector;self.actual+=r
 def diagnostics(self):return {'external_regret':float(self.cum.max()-self.actual)}

class RegretMatchingAgent:
 def __init__(self,value,grid,eta,seed):self.value=value;self.bid_grid=np.asarray(grid);self.rng=np.random.default_rng(seed);self.cum=np.zeros(len(grid));self.actual=0.
 def policy(self):
  pos=np.maximum(self.cum-self.actual,0);return pos/pos.sum() if pos.sum()>0 else np.ones(len(pos))/len(pos)
 def act(self):return float(self.rng.choice(self.bid_grid,p=self.policy()))
 def update(self,a,r,reward_vector):self.cum+=reward_vector;self.actual+=r
 def diagnostics(self):return {'external_regret':float(self.cum.max()-self.actual)}

def job_id(x):return 'run-'+hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()[:24]
def run_job(spec):
 learner,mech,v,h,ch,cl,seed,step,tail=spec;grids=[np.round(np.arange(0,1+step/2,step),10),np.round(np.arange(0,v+step/2,step),10)];etas=[ch*math.sqrt(math.log(len(grids[0]))/h),cl*math.sqrt(math.log(len(grids[1]))/h)];Cls={'hedge':HedgeAgent,'ftpl':FTPLAgent,'regret_matching':RegretMatchingAgent}[learner];agents=[Cls(1,grids[0],etas[0],2*seed),Cls(v,grids[1],etas[1],2*seed+1)];rng=np.random.default_rng(seed+10000);values=np.array([1.,v]);s={'revenue':0.,'welfare':0.,'high_win':0.};tail0=int((1-tail)*h);bidh=np.zeros(len(grids[0]));bidl=np.zeros(len(grids[1]));start=time.perf_counter()
 for t in range(h):
  bids=np.array([a.act() for a in agents]);res=run_auction(bids,mech,rng=rng);rewards=res.allocations*values-res.payments
  for i,a in enumerate(agents):a.update(bids[i],rewards[i],counterfactual_rewards(a,i,bids,mech,0,1))
  s['revenue']+=float(res.payments.sum());s['welfare']+=float(res.allocations@values);s['high_win']+=float(res.allocations[0])
  if t>=tail0:bidh[np.abs(grids[0]-bids[0]).argmin()]+=1;bidl[np.abs(grids[1]-bids[1]).argmin()]+=1
 return {'run_id':job_id(spec),'learner':learner,'mechanism':mech,'v_low':v,'horizon':h,'c_high':ch,'c_low':cl,'seed':seed,'step':step,**{k:x/h for k,x in s.items()},'regret_high':agents[0].diagnostics()['external_regret']/h,'regret_low':agents[1].diagnostics()['external_regret']/h,'tail_bid_high':bidh.tolist(),'tail_bid_low':bidl.tolist(),'runtime_seconds':time.perf_counter()-start}

def tasks(cfg):return [(l,m,e['v_low'],e['horizon'],e['c_high'],e['c_low'],s,cfg['bid_step'],cfg['tail_share'])for l in cfg['learners']for e in cfg['environments']for s in cfg['seeds']for m in cfg['mechanisms']]
def valid(path,rid):
 try:d=json.loads(path.read_text())
 except Exception:return False
 return d.get('run_id')==rid
def execute(root,cfg_path,workers=2,max_jobs=None):
 cfg=json.loads(cfg_path.read_text());ts=tasks(cfg);parts=root/'results'/'level_05'/'runs';parts.mkdir(parents=True,exist_ok=True);pending=[x for x in ts if not valid(parts/f'{job_id(x)}.json',job_id(x))];pending=pending[:max_jobs]if max_jobs else pending;start=time.perf_counter();done=0
 with ProcessPoolExecutor(max_workers=workers)as pool:
  fs={pool.submit(run_job,x):x for x in pending}
  for f in as_completed(fs):
   row=f.result();_atomic_json(parts/f"{row['run_id']}.json",row);done+=1;completed=sum(valid(parts/f'{job_id(x)}.json',job_id(x))for x in ts);_atomic_json(root/'results'/'level_05'/'checkpoint.json',{'status':'running','expected':len(ts),'completed':completed,'remaining':len(ts)-completed,'workers':workers,'config_hash':file_hash(cfg_path)})
 completed=sum(valid(parts/f'{job_id(x)}.json',job_id(x))for x in ts);status='complete'if completed==len(ts)else'shard_complete';_atomic_json(root/'results'/'level_05'/'checkpoint.json',{'status':status,'expected':len(ts),'completed':completed,'remaining':len(ts)-completed,'workers':workers,'config_hash':file_hash(cfg_path),'runtime_seconds':time.perf_counter()-start});return completed
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--workers',type=int,default=2);p.add_argument('--max-jobs',type=int);a=p.parse_args();print(execute(a.root,a.config,a.workers,a.max_jobs))

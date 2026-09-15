from abc import ABC, abstractmethod
import numpy as np


class Agent(ABC):
    def __init__(self, value, bid_grid, seed=0):
        self.value = float(value)
        self.bid_grid = np.asarray(bid_grid, dtype=float)
        self.rng = np.random.default_rng(seed)

    @abstractmethod
    def act(self): ...

    @abstractmethod
    def update(self, action, reward, reward_vector=None): ...

    def diagnostics(self): return {}

    def policy(self):
        raise NotImplementedError


class TruthfulAgent(Agent):
    def act(self): return float(self.bid_grid[np.abs(self.bid_grid - self.value).argmin()])
    def update(self, action, reward, reward_vector=None): return None
    def policy(self):
        p=np.zeros(len(self.bid_grid)); p[np.abs(self.bid_grid-self.value).argmin()]=1; return p


class EquilibriumAgent(Agent):
    def __init__(self, value, bid_grid, n_bidders=2, seed=0):
        super().__init__(value, bid_grid, seed)
        self.n_bidders = n_bidders
    def act(self):
        target = (self.n_bidders - 1) * self.value / self.n_bidders
        return float(self.bid_grid[np.abs(self.bid_grid - target).argmin()])
    def update(self, action, reward, reward_vector=None): return None
    def policy(self):
        p=np.zeros(len(self.bid_grid)); p[np.abs(self.bid_grid-self.act()).argmin()]=1; return p


class HedgeAgent(Agent):
    def __init__(self, value, bid_grid, eta=0.05, seed=0):
        super().__init__(value, bid_grid, seed); self.eta = eta; self.log_weights = np.zeros(len(self.bid_grid)); self.cumulative_rewards=np.zeros(len(self.bid_grid)); self.actual_reward=0.0
    def policy(self):
        z=self.log_weights-self.log_weights.max(); p=np.exp(z); return p/p.sum()
    def act(self):
        return float(self.rng.choice(self.bid_grid, p=self.policy()))
    def update(self, action, reward, reward_vector=None):
        if reward_vector is None: raise ValueError("Hedge requires full-information reward_vector")
        rv=np.asarray(reward_vector); self.cumulative_rewards+=rv; self.actual_reward+=reward; self.log_weights=self.eta*self.cumulative_rewards
    def diagnostics(self):
        p=self.policy(); return {"entropy":float(-np.sum(p*np.log(p+1e-15))),"external_regret":float(self.cumulative_rewards.max()-self.actual_reward)}


class Exp3Agent(Agent):
    def __init__(self, value, bid_grid, gamma=0.08, seed=0):
        super().__init__(value, bid_grid, seed); self.gamma = gamma; self.log_weights = np.zeros(len(self.bid_grid)); self.last_p = None
    def act(self):
        w = np.exp(self.log_weights-self.log_weights.max()); p = (1-self.gamma)*w/w.sum()+self.gamma/len(w); self.last_p=p
        return float(self.rng.choice(self.bid_grid, p=p))
    def update(self, action, reward, reward_vector=None):
        j = int(np.abs(self.bid_grid-action).argmin()); scaled = np.clip(reward, -1, 1)
        self.log_weights[j] += self.gamma * scaled / (len(self.bid_grid)*self.last_p[j])


class QLearningAgent(Agent):
    def __init__(self, value, bid_grid, learning_rate=0.1, epsilon=0.15, epsilon_decay=0.9999, seed=0):
        super().__init__(value, bid_grid, seed); self.lr=learning_rate; self.epsilon=epsilon; self.epsilon_decay=epsilon_decay; self.q=np.zeros(len(self.bid_grid))
    def act(self):
        if self.rng.random() < self.epsilon: return float(self.rng.choice(self.bid_grid))
        best=np.flatnonzero(self.q == self.q.max()); return float(self.bid_grid[self.rng.choice(best)])
    def update(self, action, reward, reward_vector=None):
        j=int(np.abs(self.bid_grid-action).argmin()); self.q[j] += self.lr*(reward-self.q[j]); self.epsilon *= self.epsilon_decay
    def diagnostics(self): return {"epsilon": float(self.epsilon), "max_q": float(self.q.max())}


class UCBAgent(Agent):
    def __init__(self, value, bid_grid, c=1.4, seed=0):
        super().__init__(value, bid_grid, seed); self.c=c; self.counts=np.zeros(len(self.bid_grid)); self.means=np.zeros(len(self.bid_grid)); self.t=0
    def act(self):
        unseen=np.flatnonzero(self.counts==0)
        j=int(unseen[0]) if unseen.size else int(np.argmax(self.means+self.c*np.sqrt(np.log(self.t+1)/self.counts)))
        return float(self.bid_grid[j])
    def update(self, action, reward, reward_vector=None):
        j=int(np.abs(self.bid_grid-action).argmin()); self.t+=1; self.counts[j]+=1; self.means[j]+=(reward-self.means[j])/self.counts[j]

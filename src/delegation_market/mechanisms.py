from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class AuctionResult:
    winner: int | None
    allocations: np.ndarray
    payments: np.ndarray
    price: float


def run_auction(bids, kind="first_price", reserve=0.0, alpha=1.0, rng=None):
    """Resolve a single-item auction with uniform random tie-breaking."""
    bids = np.asarray(bids, dtype=float)
    if bids.ndim != 1 or bids.size == 0 or np.any(~np.isfinite(bids)) or np.any(bids < 0):
        raise ValueError("bids must be a non-empty vector of finite non-negative values")
    if reserve < 0 or not 0 <= alpha <= 1:
        raise ValueError("reserve must be non-negative and alpha must lie in [0, 1]")
    eligible = np.flatnonzero(bids >= reserve)
    allocations = np.zeros(bids.size, dtype=float)
    payments = np.zeros(bids.size, dtype=float)
    if eligible.size == 0:
        return AuctionResult(None, allocations, payments, 0.0)
    rng = np.random.default_rng() if rng is None else rng
    top = bids[eligible].max()
    winner = int(rng.choice(eligible[bids[eligible] == top]))
    allocations[winner] = 1.0
    losing = np.delete(bids, winner)
    second = float(losing.max()) if losing.size else 0.0
    if kind in {"first_price", "reserve_first_price"}:
        price = float(bids[winner])
    elif kind in {"second_price", "reserve_second_price"}:
        price = max(float(reserve), second)
    elif kind == "hybrid":
        price = max(float(reserve), alpha * float(bids[winner]) + (1 - alpha) * second)
    elif kind == "all_pay":
        payments[:] = bids
        return AuctionResult(winner, allocations, payments, float(payments.sum()))
    else:
        raise ValueError(f"unknown mechanism: {kind}")
    payments[winner] = price
    return AuctionResult(winner, allocations, payments, price)


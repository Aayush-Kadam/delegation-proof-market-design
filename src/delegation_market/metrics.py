import numpy as np


def summarize(values, bids, allocations, payments):
    values=np.asarray(values); bids=np.asarray(bids); allocations=np.asarray(allocations); payments=np.asarray(payments)
    welfare=(values*allocations).sum(axis=1); optimal=values.max(axis=1)
    efficient=(allocations.argmax(axis=1)==values.argmax(axis=1)).astype(float)
    utilities=allocations*values-payments
    revenue=payments.sum(axis=1)
    return {
        "mean_welfare": float(welfare.mean()), "welfare_ratio": float((welfare/np.maximum(optimal,1e-12)).mean()),
        "allocative_efficiency": float(efficient.mean()), "mean_revenue": float(revenue.mean()),
        "mean_bidder_surplus": float(utilities.sum(axis=1).mean()), "mean_bid_shading": float((values-bids).mean()),
        "win_shares": allocations.mean(axis=0).tolist(),
    }


def delegation_gap(benchmark, delegated): return float(benchmark-delegated)


def price_of_delegation(benchmark, delegated):
    return float(benchmark/delegated) if abs(delegated)>1e-12 else float("nan")


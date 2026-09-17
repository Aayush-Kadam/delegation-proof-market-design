"""Deterministic M5 checks for the restricted two-round conflict theorem."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def softmax(xs):
    z = max(xs)
    w = [math.exp(x-z) for x in xs]
    s = sum(w)
    return [x/s for x in w]


def state_after_round_one(v: float, eta_h: float, eta_l: float, mechanism: str):
    if mechanism == "first_price":
        q = softmax([eta_h/4, 3*eta_h*(1-v)/4, 0])
        p = 1/(1+math.exp(eta_l*v/6))
    elif mechanism == "second_price":
        q = softmax([eta_h/4, eta_h*(3-v)/4, eta_h*(1-v/2)])
        p = 1/(1+math.exp(-eta_l*v/6))
    else:
        raise ValueError(mechanism)
    return q, p


def round_metrics(v, q, p, mechanism):
    allocation = .5*(1-p)*q[0] + (1-.5*p)*q[1] + q[2]
    if mechanism == "first_price":
        revenue = v*(q[1]+p*q[0])+q[2]
    else:
        revenue = v*p*(q[1]+q[2])
    return revenue, allocation


def two_round_contrast(v: float, eta_h: float, eta_l: float):
    qf, pf = state_after_round_one(v, eta_h, eta_l, "first_price")
    qs, ps = state_after_round_one(v, eta_h, eta_l, "second_price")
    rf, af = round_metrics(v, qf, pf, "first_price")
    rs, ass = round_metrics(v, qs, ps, "second_price")
    # Uniform round-one values: RF=(3v+2)/6, RS=v/3, allocation=2/3.
    return {
        "v": v, "eta_high": eta_h, "eta_low": eta_l,
        "delta_revenue": ((3*v+2)/6 + rf - v/3 - rs)/2,
        "delta_allocation_spa_minus_fpa": (ass-af)/2,
        "phi_round_two_allocation": ass-af,
    }


def analyze(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    representative = [two_round_contrast(v, e, e) for v in (.3, .5, .7) for e in (.5, 1., 2.)]
    with (output/"restricted_two_round_table.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=representative[0]); w.writeheader(); w.writerows(representative)

    # 750 deterministic environments, below the preregistered 1,000 cap.
    scan=[]
    for iv in range(25):
        v=.05+.9*iv/24
        for eh in (.25,.5,1.,2.,4.):
            for el in (.25,.5,1.,2.,4.,8.):
                scan.append(two_round_contrast(v,eh,el))
    with (output/"counterexample_scan.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=scan[0]); w.writeheader(); w.writerows(scan)
    point=two_round_contrast(1/3,1,.1)
    verdict={
        "environments":len(scan),
        "conflict_count":sum(x["delta_revenue"]>0 and x["delta_allocation_spa_minus_fpa"]>0 for x in scan),
        "smallest_allocation_counterexample":min(scan,key=lambda x:x["delta_allocation_spa_minus_fpa"]),
        "certificate_point":point,
        "known_m4_counterexample_preserved":{"v":.75,"H":1600,"c_high":1,"c_low":2},
    }
    (output/"verdict.json").write_text(json.dumps(verdict,indent=2)+"\n",encoding="utf-8")
    return verdict


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,required=True)
    print(json.dumps(analyze(p.parse_args().output),indent=2))

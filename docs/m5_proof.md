# Proof of TH-M5-003

Let `H` and `L` have values `1` and `v`, action sets `{0,v,1}` and `{0,v}`, and uniform initial weights. Ties are fair. All quantities below are expectations under independent mean-field mixing.

## Lemma 1 — Hedge ratios

For full-information Hedge, `w_i^{t+1}(b)=w_i^t(b)exp(eta_i u_i^t(b))`. Iteration and division give

`log[w_i^t(a)/w_i^t(b)]=log[w_i^1(a)/w_i^1(b)]+eta_i sum_{s<t}(u_i^s(a)-u_i^s(b))`.

## Lemma 2 — first-round payoffs

Direct enumeration gives high-bidder payoff vectors

`FPA: (1/4,3(1-v)/4,0)`, `SPA: (1/4,(3-v)/4,1-v/2)`,

and low-bidder vectors

`FPA: (v/6,0)`, `SPA: (v/6,v/3)`.

The first-round allocation is `2/3` in both mechanisms. Revenues are `(3v+2)/6` and `v/3`, so FPA's first-round advantage is `(v+2)/6`.

## Lemma 3 — exact round-two state

Lemma 1 with uniform weights yields

`Q_F=softmax(eta_H(1/4,3(1-v)/4,0))`, `p_F=[1+exp(eta_L v/6)]^{-1}`,

`Q_S=softmax(eta_H(1/4,(3-v)/4,1-v/2))`, `p_S=[1+exp(-eta_L v/6)]^{-1}`.

No approximation enters these identities.

## Lemma 4 — outcome formulas

For `Q=(q_0,q_v,q_1)` and low bid-`v` probability `p`, high-bidder allocation is

`A(Q,p)=q_0(1-p)/2+q_v(1-p/2)+q_1`.

Round-two revenues are `v(q_Fv+p_F q_F0)+q_F1` in FPA and `v p_S(q_Sv+q_S1)` in SPA.

## Theorem — restricted finite-horizon delegation conflict

Define `Phi=A(Q_S,p_S)-A(Q_F,p_F)` and

`C_2={(v,eta_H,eta_L):0<v<2/5, eta_H>0, eta_L>=0, Phi>0}`.

For every point of `C_2`, `A_SPA(2)-A_FPA(2)=Phi/2>0`. Since second-round FPA revenue is at least zero and second-round SPA revenue is at most `v`,

`R_FPA(2)-R_SPA(2) >= [(v+2)/6-v]/2=(2-5v)/12>0`.

Thus neither mechanism dominates both seller revenue and allocation on `C_2`.

## Certified nonemptiness and corollaries

The exact-rational interval certificate at `(1/3,1,1/10)` gives a strictly positive interval for `Phi`; continuity therefore supplies a nonempty open neighborhood. Welfare follows once, mechanically: `A_SPA>A_FPA` implies `W_SPA-W_FPA=(1-v)(A_SPA-A_FPA)>0`. Total bidder-surplus comparisons require the separate identity already proved in M4 and are not part of this theorem.

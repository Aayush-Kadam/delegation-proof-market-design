# DELEGATION-PROOF MARKET DESIGN — M6 THEORY STATUS

## 1. Executive verdict

**MODERATE THEORY ADVANCE**

M6 proves that the M5 phenomenon is not a two-round curiosity. The same three-by-two model has a rigorously certified closed parameter rectangle on which the conflict holds for every horizon from 2 through 9.

## 2. Strongest theorem

**TH-M6-003 (finite-horizon rectangle theorem).** Under the M5 assumptions—persistent values `(1,v)`, high actions `{0,v,1}`, low actions `{0,v}`, fair ties, uniform weights, and deterministic full-information Hedge—suppose

`v in [0.30,0.36]`, `eta_H in [0.8,1.2]`, `eta_L in [0.05,0.15]`.

Then for every integer `H in {2,...,9}`,

`R_FPA(H)>R_SPA(H)` and `A_SPA(H)>A_FPA(H)`.

Consequently `W_SPA(H)>W_FPA(H)`. The certified worst-case interval lower bounds are positive at every covered horizon. At `H=9` they are `0.157332...` for revenue and `0.00827648...` for allocation.

## 3. Exact recurrence

Let `x=log(w_H(1)/w_H(v))`, `y=log(w_H(v)/w_H(0))`, and `z=log(w_L(v)/w_L(0))`. Then

`q=(1,e^y,e^(x+y))/(1+e^y+e^(x+y))`, `p=e^z/(1+e^z)`.

Both mechanisms have `u_H(0)=(1-p)/2`. In FPA,

`u_H(v)=(1-v)(1-p/2)`, `u_H(1)=0`, `z' = z-eta_L v q_0/2`.

In SPA,

`u_H(v)=1-p(1+v)/2`, `u_H(1)=1-vp`, `z' = z+eta_L v q_0/2`.

For either mechanism,

`x'=x+eta_H[u_H(1)-u_H(v)]`, `y'=y+eta_H[u_H(v)-u_H(0)]`.

These identities are exact and generate every finite-horizon result.

## 4. Certification

The complete rectangle was partitioned into `12x8x5=480` closed subboxes. A 70-digit outward-enclosed Decimal interval recurrence was applied to every subbox. Every elementary operation is expanded to adjacent representable decimals; Decimal exponential evaluation is correctly rounded. This proves coverage of the continuum, not merely grid points.

The same certificate becomes inconclusive for allocation at `H=10`: its enclosure crosses zero. This is interval dependency, not a counterexample, so the theorem stops at `H=9`.

## 5. Monotonicity and mechanism

The low bidder's log ratio is globally monotone: it decreases in FPA and increases in SPA whenever `q_0>0`. FPA bid `1` always has zero utility; SPA bid `1` has utility `1-vp>0`. These exact signs explain divergent mass movement. Global monotonicity of the final revenue/allocation contrast in each parameter was not proved, so certification used exhaustive interval subdivision rather than corner-only reasoning.

## 6. Horizon ladder and limitations

The M5 witness `(1/3,1,.1)` retains both signs numerically through `H=100`; this is numerical support only. The theorem covers `H<=9`. It does not explain the Level-3 `.01` grid or upper interior values around `.5` and `.7`.

An exact closed-form horizon formula was not obtained. A generic payment bound only recovers the two-round result and is too loose thereafter.

## 7. Richer grids and full-grid bridge

No richer-grid theorem is claimed. Extra actions destroy the exact three-state recurrence and uniform-initialization accounting used by the certificate. An off-core mass bound also cannot follow from Hedge alone at early horizons: every added action begins with positive uniform mass, and payoff gaps need not be uniformly positive. Thus the full-grid bridge remains **PARTIAL** at the structural-obstruction level, not proved.

## 8. Counterexamples

- Universal revenue dominance remains false by the M4 point `(.75,1600,1,2)`.
- The symmetric two-action reduction still fails the allocation sign.
- The M5 deterministic scan gives allocation failure at `(.95,.25,8)` for `H=2`.
- `H=10` is not disproved; it is outside the current rigorous certificate.

## 9. Theory level

**LEVEL C.** M6 includes Level B (an explicit rectangle) and proves the conflict for every `H=2,...,9`. It does not reach a general closed-form Level-D horizon bound or a richer-grid Level-E theorem.

## 10. Literature novelty

**POSSIBLY DISTINCT.** Targeted rechecking found no prior theorem matching an explicit closed rectangle and consecutive finite-horizon FPA-versus-SPA revenue/allocation reversal under exact Hedge dynamics. The result remains narrow relative to asymptotic auction-learning and revenue-only guarantees.

## 11. Publication readiness and gate

Publication readiness: **6/10** (previously 5/10).

Next gate: **STRENGTHEN THEORY ONCE MORE**. The priority is either a sharper interval/analytic argument beyond `H=9` or a controlled four-action high-bidder bridge—not cross-learner validation yet.

## 12. Next-phase budget

At most 1,000 deterministic configurations, zero seeds, horizons up to 10,000 only for recurrence diagnostics, and under 30 minutes expected machine time. No next phase has begun.

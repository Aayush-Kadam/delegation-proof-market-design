# Research specification (v0.1)

## Frozen baseline

Two bidders, fixed private values `(1.0, 0.6)`, public bid grid `{0,.01,...,1}`, winner utility `x_i(v_i-p_i)`, uniform random tie-breaking, 10,000 development rounds, and independent deterministic seeds. Baseline mechanisms are first-price and second-price. Reserve and hybrid mechanisms are extensions.

## Claim taxonomy

- **ESTABLISHED:** directly supported by cited prior work.
- **REPLICATED:** an established target reproduced by this code under documented differences.
- **NEW COMPUTATIONAL RESULT:** a preregistered, multi-seed result surviving robustness and novelty checks.
- **THEORETICAL RESULT:** a formal statement with a checked proof.

The initial release contains established context and infrastructure only. Smoke output is diagnostic, not evidence of novelty.

## Identification limits

Fixed-value repeated play is a complete-information stage game and must not be conflated with the symmetric Bayesian IPV benchmark. Low revenue, correlation, or alternation alone is not collusion. Revenue and welfare are reported separately.


# Event-window robustness (extended sample)

_Generated 2026-06-02 21:11:27_  

Same Fama-MacBeth quarterly regression as LM (2011) Tables IV/V col (2) and (4),
re-fit for five different LHS event-windows. Each cell shows `t (adj R²)`.
The [0,+3] column is LM's canonical 4-day filing-period window.


## IV_col2_prop  (LHS scope: full, x = `fin_neg_prop`)

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 50,681 | -1.47 (1.85%) | -3.04 (2.29%) | -2.45 (2.42%) |
| post_LM (24q) | 17,363 | +1.31 (3.42%) | +1.16 (4.58%) | +1.35 (5.13%) |
| algo_era (20q) | 13,127 | +0.72 (6.56%) | +0.90 (7.57%) | +1.89 (7.87%) |
| covid_recent (6q) | 1,242 | +2.38 (2.58%) | +0.36 (-0.46%) | -0.90 (9.53%) |
| full (110q) | 82,413 | -0.16 (3.08%) | -1.68 (3.77%) | -1.05 (4.62%) |

## IV_col4_tfidf  (LHS scope: full, x = `fin_neg_tfidf_full`)

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 50,681 | -1.66 (1.99%) | -2.76 (2.52%) | -2.25 (2.69%) |
| post_LM (24q) | 17,363 | +0.17 (3.36%) | +0.41 (4.53%) | +0.52 (5.04%) |
| algo_era (20q) | 13,127 | +0.77 (6.86%) | +1.21 (8.06%) | +1.97 (8.38%) |
| covid_recent (6q) | 1,242 | -0.05 (2.89%) | -2.53 (0.32%) | -2.03 (9.66%) |
| full (110q) | 82,413 | -1.04 (3.26%) | -1.80 (4.00%) | -1.32 (4.78%) |

## V_col2_prop_MDA  (LHS scope: MDA, x = `fin_neg_prop_mda`)

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 48,134 | -2.11 (1.71%) | -3.54 (2.37%) | -3.07 (2.43%) |
| post_LM (24q) | 17,241 | -0.70 (3.19%) | -0.63 (4.40%) | +0.36 (4.78%) |
| algo_era (20q) | 13,044 | -2.77 (6.51%) | -2.04 (7.36%) | -1.73 (7.73%) |
| covid_recent (6q) | 1,237 | -0.10 (7.48%) | +1.20 (2.42%) | +1.81 (13.60%) |
| full (110q) | 79,656 | -2.81 (3.17%) | -3.41 (3.93%) | -2.58 (4.72%) |

## V_col4_tfidf_MDA  (LHS scope: MDA, x = `fin_neg_tfidf_mda`)

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 48,134 | -2.24 (1.73%) | -3.56 (2.46%) | -3.03 (2.52%) |
| post_LM (24q) | 17,241 | -1.48 (3.17%) | -1.72 (4.36%) | +0.18 (4.74%) |
| algo_era (20q) | 13,044 | -1.38 (6.63%) | -0.96 (7.52%) | -0.69 (7.56%) |
| covid_recent (6q) | 1,237 | -0.06 (3.96%) | -0.00 (3.27%) | +1.20 (14.88%) |
| full (110q) | 79,656 | -2.90 (3.04%) | -3.81 (4.09%) | -2.74 (4.79%) |

# Robustness check: longer event windows — extended sample (1994–2024)

_Generated 2026-10-25 10:51:21_  

Same Fama-MacBeth quarterly regression as in the headline, re-fit with
[0,+10] and [0,+20] excess returns. Each cell shows `t-stat (adj R²)`.
These horizons also absorb post-filing drift and unrelated news.


## Fin-Neg proportional, full 10-K text

| Subperiod (n_qtrs) | n (canonical) | [0,+10] | [0,+20] |
|---|---:|---:|---:|
| LM_in_sample (60q) | 50,681 | -1.24 (3.82%) | +0.13 (5.77%) |
| post_LM (24q) | 17,363 | +1.53 (7.34%) | +0.85 (8.84%) |
| algo_era (20q) | 13,525 | +1.50 (7.98%) | -0.02 (8.17%) |
| covid_recent (19q) | 13,641 | -1.09 (3.67%) | -0.69 (6.71%) |
| full (123q) | 95,210 | -0.42 (5.20%) | +0.11 (6.93%) |

## Fin-Neg tf-idf, full 10-K text

| Subperiod (n_qtrs) | n (canonical) | [0,+10] | [0,+20] |
|---|---:|---:|---:|
| LM_in_sample (60q) | 50,681 | -1.37 (3.96%) | -0.45 (5.99%) |
| post_LM (24q) | 17,363 | +0.89 (7.35%) | +0.32 (8.76%) |
| algo_era (20q) | 13,525 | +2.16 (8.03%) | -0.02 (8.22%) |
| covid_recent (19q) | 13,641 | -2.49 (4.06%) | -2.08 (6.98%) |
| full (123q) | 95,210 | -0.84 (5.36%) | -0.85 (7.07%) |

## Fin-Neg proportional, MD&A section only

| Subperiod (n_qtrs) | n (canonical) | [0,+10] | [0,+20] |
|---|---:|---:|---:|
| LM_in_sample (60q) | 48,134 | -2.37 (3.79%) | -1.59 (5.57%) |
| post_LM (24q) | 17,241 | +0.85 (6.98%) | +1.11 (8.36%) |
| algo_era (20q) | 13,441 | -1.29 (7.70%) | -1.37 (7.96%) |
| covid_recent (19q) | 13,553 | +2.90 (3.75%) | +2.78 (6.75%) |
| full (123q) | 92,369 | -1.11 (5.07%) | -0.41 (6.70%) |

## Fin-Neg tf-idf, MD&A section only

| Subperiod (n_qtrs) | n (canonical) | [0,+10] | [0,+20] |
|---|---:|---:|---:|
| LM_in_sample (60q) | 48,134 | -2.17 (3.86%) | -1.22 (5.60%) |
| post_LM (24q) | 17,241 | +0.98 (6.97%) | +1.66 (8.17%) |
| algo_era (20q) | 13,441 | +0.22 (7.68%) | -0.64 (7.96%) |
| covid_recent (19q) | 13,553 | +0.22 (4.01%) | -0.41 (6.58%) |
| full (123q) | 92,369 | -1.73 (5.12%) | -1.08 (6.65%) |

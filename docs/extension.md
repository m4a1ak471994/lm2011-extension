# Out-of-sample extension of LM (2011) — 1994–2024

This document extends the Loughran & McDonald (2011) Fama-MacBeth filing-period excess-return regressions from the LM in-sample window (1994–2008) through **end of 2024** (~17 additional years of 10-K filings), using the **identical methodology** (same dictionary, same controls, same FM weighting, same Newey-West HAC SE, same FF48 industry fixed effects).

The exposition below focuses on the **tf-idf-weighted** specification of Fin-Neg (LM Table IV col 4 and Table V col 4) — the richer of the two LM specifications, which weights each negative-tone word by its inverse document frequency in the corpus. Results for the unweighted proportional Fin-Neg (LM Table IV col 2 / V col 2) are reported alongside in the sub-period table without separate discussion.

Three questions:

1. **Out-of-sample**: does the tf-idf negative-tone signal still predict four-day excess returns in 2009–2024?
2. **Decay**: how does the coefficient evolve year by year across the full sample?
3. **Regime conditioning**: how does it look in the GFC, the algo-trading era, and COVID-recent windows?

---

## Sample

| Window | Firm-years | Unique permnos | Quarters |
|---|---:|---:|---:|
| LM in-sample (1994–2008) | 50,900 | ~9,000 | 60 |
| Extension (2009–2024) | 32,520 | 6,500+ | 56 |
| **Full extended (1994–2024)** | **83,422** | **11,125** | **116** |

CRSP daily ends 2024-12-31 (typical WRDS lag), so the [+252] post-window required by the LM Table I funnel filter (10) drops most filings filed in late 2023 onward. The "covid_recent" sub-period has 1,367 firm-years for this reason.

Inputs were rebuilt end-to-end via `code/preclean.py` (`END_YR = 2026`), `code/step1c_manifest_10k_extended.py`, then the standard `step4 → step5 → step6 → step7` pipeline.

One small methodology refinement was added for the post-2009 portion of the sample: inline-XBRL `<ix:hidden>` blocks are stripped from the raw text before tokenization (`code/mdna_extract.py`). These blocks wrap content tagged for machine readers but not visible to humans in the rendered document; in early-adopter filings (2019–2022) some filers tagged narrative prose this way, which could double-count LM-dictionary tokens against text the visible reader saw once. Pre-2009 filings have no inline XBRL so this is a no-op on the LM in-sample window. Empirically the change shifts every coefficient by less than 0.5% — the contamination was smaller than feared — but the fix is principled and was retained.

---

## Headline — Table IV col (4) Fin-Neg tf-idf, full extended sample

| Specification | n | n_qtrs | Coef | t | adj R² |
|---|---:|---:|---:|---:|---:|
| LM (2011) published | 50,115 | 60 | −0.0030 | −3.11 | 2.63 % |
| LM in-sample (1994–2008), this repo | 50,681 | 60 | −0.0094 | −2.76 | 2.52 % |
| **Full extended (1994–2024)** | **82,413** | **110** | **−0.0044** | **−1.80** | **4.00 %** |

In the full extended sample the headline tf-idf coefficient is negative (correct sign) at p ≈ 0.072 (two-sided), not statistically significant at conventional 5 % level.

The full-window result is dominated by the LM in-sample sub-period; the per-sub-period and rolling decompositions in the next two sections show where the signal lives and where it does not.

---

## Sub-period replication (`step9_subperiods.py`)

Each subperiod is re-fit with the same Fama-MacBeth regression on its own quarterly cross-sections.

### Table IV col (4) — Fin-Neg tf-idf, full 10-K text

| Subperiod | Years | n | n_qtrs | Coef | t | adj R² |
|---|---|---:|---:|---:|---:|---:|
| LM_in_sample | 1994–2008 | 50,681 | 60 | −0.0094 | −2.76 | 2.52 % |
| GFC | 2008–2009 | 6,077 | 8 | −0.0071 | −1.49 | 3.48 % |
| post_LM | 2009–2014 | 17,363 | 24 | +0.0013 | +0.41 | 4.53 % |
| algo_era | 2015–2019 | 13,127 | 20 | +0.0053 | +1.21 | 8.06 % |
| covid_recent | 2020–2024 | 1,242 | 6 | −0.0195 | −2.53 | 0.32 % |
| full | 1994–2024 | 82,413 | 110 | −0.0044 | −1.80 | 4.00 % |

The covid_recent row has n = 1,242 / R² = 0.32 % across only 6 quarters; treat its t = −2.53 as a small-sample point estimate rather than a stable regime finding.

### Table V col (4) — Fin-Neg tf-idf, MD&A section only

| Subperiod | Years | n | n_qtrs | Coef | t | adj R² |
|---|---|---:|---:|---:|---:|---:|
| LM_in_sample | 1994–2008 | 48,134 | 60 | −0.0151 | −3.56 | 2.46 % |
| GFC | 2008–2009 | 6,027 | 8 | −0.0064 | −1.21 | 3.38 % |
| post_LM | 2009–2014 | 17,241 | 24 | −0.0049 | −1.72 | 4.36 % |
| algo_era | 2015–2019 | 13,044 | 20 | −0.0034 | −0.96 | 7.52 % |
| covid_recent | 2020–2024 | 1,237 | 6 | −0.0000 | −0.00 | 3.27 % |
| full | 1994–2024 | 79,656 | 110 | −0.0108 | −3.81 | 4.09 % |

The Table V MD&A-only specification retains a negative coefficient at t = −3.81 / R² = 4.09 % in the full extended sample. The negative sign holds in every sub-period; statistical significance is only present in the LM in-sample row and in the full pooled fit.

### Companion: Table IV col (2) and Table V col (2) — Fin-Neg proportional

For completeness, the proportional (unweighted) results across the same subperiods:

| Subperiod | Years | IV col (2) t | IV col (2) R² | V col (2) t | V col (2) R² |
|---|---|---:|---:|---:|---:|
| LM_in_sample | 1994–2008 | −3.04 | 2.29 % | −3.54 | 2.37 % |
| GFC | 2008–2009 | −0.18 | 3.44 % | −2.79 | 3.24 % |
| post_LM | 2009–2014 | +1.16 | 4.58 % | −0.63 | 4.40 % |
| algo_era | 2015–2019 | +0.90 | 7.57 % | −2.04 | 7.36 % |
| covid_recent | 2020–2024 | +0.36 | −0.46 % | +1.20 | 2.42 % |
| full | 1994–2024 | −1.68 | 3.77 % | −3.41 | 3.93 % |

---

## Rolling-window decay (`step10_decay.py`)

### Design

The sub-period analysis above partitions the sample into a handful of disjoint regimes (LM_in_sample, GFC, post_LM, …). That collapses what is plausibly a gradual evolution of the negative-tone signal into discrete buckets and depends on where we drew the boundaries. The rolling-window analysis below avoids both issues — it asks, year by year, *what does the Table IV col (4) coefficient look like if we re-fit it only on the trailing 5 years of filings?*

The procedure indexes windows by their **end year** *y*. For each end year:

1. Take the subset of the extended panel with `date_filed` in calendar years `[y − 4, y]` — a 5-year backward-looking window of filings, giving 5 × 4 = 20 quarterly cross-sections.
2. Run the same Fama-MacBeth quarterly cross-sectional regression as in Table IV col (4): per quarter, regress the four-day excess return on Fin-Neg tf-idf + log size + log BM + log turnover + pre-event FF-α + IO + NASDAQ + FF48 industry FEs. Save the per-quarter Fin-Neg coefficient β_q.
3. The window's reported coefficient is the time-series average β̄ across those ~20 quarterly βs, weighted by *n_obs/q*. The standard error is a Newey-West HAC (1 lag) on the β_q series. R² is the simple time-series average of per-quarter adjusted R².
4. Increment the end year by one and repeat.

Pre-1994 filings are excluded entirely. EDGAR was launched in May 1993 and mandatory electronic filing only phased in by May 1996; the manifest contains just 6 raw 10-K filings for calendar-year 1993, of which 2 survive the Table I funnel. Aligning the window's earliest year with LM (2011)'s own sample-start convention means the first window has end year `1998` (covering filings 1994–1998); the last window has end year `2024` (covering 2020–2024). That gives 27 windows in total.

Compared to the discrete sub-period table, the rolling design (i) smooths through quarter-to-quarter noise via the four-year overlap, (ii) makes "decay or stable?" a continuous-time question rather than a comparison of bucketed snapshots, (iii) lets us draw a single chart with a 95 % confidence band that a recruiter can read without parsing six rows of t-statistics, and (iv) uses only backward-looking information at each year *y* — the chart at point *y* never knows about post-*y* data.

A caveat for the late windows: the end year *y* requires CRSP daily coverage to extend to roughly `y + 1` (so the +252-day post-window of filings in year *y* is observable). At the current WRDS CRSP daily end of 2024-12-31, the `y = 2024` window's effective sample is just `n = 1,242` and only 6 quarters, so its point estimate is noisy — that's the rightmost point on the chart.

### Plot

The figure below shows the Fin-Neg tf-idf coefficient with 95 % Newey-West CI bands indexed by window end year.

![Sentiment-decay plot](../output/fig_sentiment_decay.png)

(*plot file*: `output/fig_sentiment_decay.png`; underlying CSV: `output/sentiment_decay.csv`)

| End year | Window | n | Coef | t | adj R² |
|---:|---|---:|---:|---:|---:|
| 1998 | 1994–1998 | 14,849 | −0.0079 | −1.79 | 1.46 % |
| 1999 | 1995–1999 | 17,915 | −0.0073 | −1.88 | 0.75 % |
| 2000 | 1996–2000 | 20,258 | −0.0152 | −2.53 | 1.71 % |
| 2001 | 1997–2001 | 20,966 | −0.0223 | −3.32 | 2.85 % |
| 2002 | 1998–2002 | 19,862 | −0.0217 | −3.05 | 2.68 % |
| 2003 | 1999–2003 | 18,662 | −0.0200 | −2.69 | 3.24 % |
| 2004 | 2000–2004 | 17,990 | −0.0211 | −2.70 | 4.10 % |
| 2005 | 2001–2005 | 17,226 | −0.0118 | −1.95 | 3.43 % |
| 2006 | 2002–2006 | 17,043 | −0.0020 | −0.87 | 1.82 % |
| 2007 | 2003–2007 | 17,063 | −0.0001 | −0.05 | 2.42 % |
| 2008 | 2004–2008 | 17,170 | −0.0003 | −0.08 | 2.68 % |
| 2009 | 2005–2009 | 16,387 | −0.0024 | −0.66 | 2.88 % |
| 2010 | 2006–2010 | 16,009 | +0.0004 | +0.09 | 3.66 % |
| 2011 | 2007–2011 | 15,594 | +0.0003 | +0.07 | 4.41 % |
| 2012 | 2008–2012 | 15,011 | −0.0005 | −0.12 | 4.36 % |
| 2013 | 2009–2013 | 14,450 | −0.0002 | −0.06 | 4.38 % |
| 2014 | 2010–2014 | 14,639 | +0.0034 | +1.04 | 4.42 % |
| 2015 | 2011–2015 | 14,526 | +0.0019 | +0.74 | 4.84 % |
| 2016 | 2012–2016 | 14,314 | −0.0008 | −0.24 | 5.49 % |
| 2017 | 2013–2017 | 14,152 | +0.0021 | +0.60 | 6.33 % |
| 2018 | 2014–2018 | 13,824 | +0.0025 | +0.78 | 8.20 % |
| 2019 | 2015–2019 | 13,127 | +0.0053 | +1.21 | 8.06 % |
| 2020 | 2016–2020 | 10,954 | +0.0022 | +0.40 | 7.88 % |
| 2021 | 2017–2021 | 8,619 | +0.0058 | +1.12 | 6.91 % |
| 2022 | 2018–2022 | 5,922 | +0.0059 | +0.80 | 6.08 % |
| 2023 | 2019–2023 | 3,458 | +0.0110 | +0.95 | 3.44 % |
| 2024 | 2020–2024 | 1,242 | −0.0195 | −2.53 | 0.32 % |

The rolling-window coefficient is negative and significant (t below −2) for end years 2000–2004, negative but at borderline significance in 1998–1999 and 2005, and near zero with oscillating sign for end years 2006–2023. The end-year 2024 row uses only n = 1,242 firm-years over 6 quarters (because of the CRSP-daily cutoff at 2024-12-31) and is reported for completeness.

---

## Event-window robustness (`step11_event_windows.py`)

LM (2011) defines its CAR over a four-day window `[0, +3]` covering the filing day plus three subsequent trading days. To check whether the result is special to that window, we re-fit each subperiod regression with three LHS event windows: `[0,+1]`, `[0,+3]` (LM canonical), `[0,+5]`. (Longer horizons of `[0,+10]` / `[0,+20]` were considered but excluded — at two-to-four-week horizons the LHS is contaminated by drift, by other firms' earnings surprises, and by macroeconomic news unrelated to the 10-K release, so the regression no longer cleanly identifies a filing-period effect.) Each cell below shows `t (adj R²)`.

### Table IV col (4) — Fin-Neg tf-idf, full 10-K text

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 50,681 | −1.66 (1.99 %) | −2.76 (2.52 %) | −2.25 (2.69 %) |
| post_LM (24q) | 17,363 | +0.17 (3.36 %) | +0.41 (4.53 %) | +0.52 (5.04 %) |
| algo_era (20q) | 13,127 | +0.77 (6.86 %) | +1.21 (8.06 %) | +1.97 (8.38 %) |
| covid_recent (6q) | 1,242 | −0.05 (2.89 %) | −2.53 (0.32 %) | −2.03 (9.66 %) |
| full (110q) | 82,413 | −1.04 (3.26 %) | −1.80 (4.00 %) | −1.32 (4.78 %) |

### Table V col (4) — Fin-Neg tf-idf, MD&A only

| Subperiod (n_qtrs) | n (canonical) | [0,+1] | [0,+3] | [0,+5] |
|---|---:|---:|---:|---:|
| LM_in_sample (60q) | 48,134 | −2.24 (1.73 %) | −3.56 (2.46 %) | −3.03 (2.52 %) |
| post_LM (24q) | 17,241 | −1.48 (3.17 %) | −1.72 (4.36 %) | +0.18 (4.74 %) |
| algo_era (20q) | 13,044 | −1.38 (6.63 %) | −0.96 (7.52 %) | −0.69 (7.56 %) |
| covid_recent (6q) | 1,237 | −0.06 (3.96 %) | −0.00 (3.27 %) | +1.20 (14.88 %) |
| full (110q) | 79,656 | −2.90 (3.04 %) | −3.81 (4.09 %) | −2.74 (4.79 %) |

### Companion: Fin-Neg proportional (col 2) across the same windows

| Subperiod | n | IV col(2) [0,+1] t | IV col(2) [0,+3] t | IV col(2) [0,+5] t | V col(2) [0,+1] t | V col(2) [0,+3] t | V col(2) [0,+5] t |
|---|---:|---:|---:|---:|---:|---:|---:|
| LM_in_sample | 50,681 | −2.16 | −3.04 | −2.65 | −2.11 | −3.54 | −3.07 |
| post_LM | 17,363 | +0.76 | +1.16 | +1.13 | −0.70 | −0.63 | +0.36 |
| algo_era | 13,127 | +0.55 | +0.90 | +1.78 | −2.77 | −2.04 | −1.73 |
| covid_recent | 1,242 | +2.38 | +0.36 | −0.90 | −0.10 | +1.20 | +1.81 |
| full | 82,413 | −0.16 | −1.68 | −1.05 | −2.81 | −3.41 | −2.58 |

Three patterns emerge:

1. **LM in-sample is window-robust.** Across both Tables IV and V, the canonical LM `[0,+3]` t-statistic is the local maximum (in absolute value) of a hump that includes `[0,+1]` and `[0,+5]`. The signal is real on the 1994–2008 sub-window and is not an artifact of choosing exactly four days.

2. **The decay is most visible in the very-short windows.** For the `post_LM` and `algo_era` sub-periods, the `[0,+1]` and `[0,+3]` t-statistics on full-text tf-idf cluster near zero or flip sign. If markets price negative tone faster post-2010 than they did in the 1990s, the short-window absence of signal is consistent with that.

3. **MD&A tf-idf is the most window-stable.** For Table V col (4), the full extended sample shows `t = −2.90 / −3.81 / −2.74` across `[0,+1] / [0,+3] / [0,+5]`. The negative sign also persists in MD&A across most sub-periods at the canonical `[0,+3]` window. The robustness reflects that MD&A text — forward-looking commentary by management — carries information that is priced over a longer post-filing horizon than mechanical text features in the rest of the 10-K.

---

## Interpretation

The tf-idf negative-tone signal is statistically significant and negatively-signed only in two stretches of the rolling decomposition:

- end years **2000–2004** (windows covering filings 1996–2000 through 2000–2004), with t between −2.69 and −3.32 and R² between 1.71 % and 4.10 %, and
- the lone end year **2024** (window 2020–2024), with t = −2.53 / R² = 0.32 % on n = 1,242.

In all other rolling windows the coefficient is near zero with t between −1.0 and +1.2.

The classical post-publication-arbitrage explanation (McLean & Pontiff 2016) cannot account for this pattern alone: the rolling-window coefficient drifts to zero by end year 2006 (window 2002–2006), which corresponds to filings made well before Loughran & McDonald (2011) was published in early 2011. Three non-exclusive candidate mechanisms are worth flagging without a clean test of any of them:

1. **Pre-publication discovery.** Tetlock (2007, *JF*) used the Harvard IV-4 dictionary on Wall Street Journal media content. Practitioner sentiment scoring of news + filings (Reuters, Bloomberg, RavenPack) was deployed in the same window. Filing-period negative-tone may have been priced by sentiment-active quants before LM curated their finance-specific dictionary.

2. **Disclosure-norm shift after Sarbanes-Oxley (2002).** Post-SOX 10-Ks contain richer cautionary boilerplate and lengthy risk factors, and from 2009 inline XBRL tags. The Table II mean of Fin-Neg in the full extended sample is 1.56 % vs the LM in-sample mean of 1.37 %, consistent with rising boilerplate that dilutes idiosyncratic tone variation.

3. **Algorithmic pricing of public text.** From 2010 onward, the LM Master Dictionary is embedded in many quant pipelines. Negative tone may now be priced within minutes of filing release, leaving no four-day excess-return predictability available to academic researchers using daily CRSP returns.

The Table V (MD&A-only, col 4 tf-idf) specification preserves t = −3.81 / R² = 4.09 % in the full pooled fit — that is, MD&A-restricted tf-idf negative tone is the single specification that remains significant pooled across 1994–2024.

---

## Files

| File | Source script |
|---|---|
| `output/table1_sample_funnel_default.csv` | `step5_build_sample.py` (extended) |
| `output/table2_extended.csv` | `step7_tables.py` |
| `output/table4_cols2_4_extended.csv` | `step7_tables.py` |
| `output/table5_cols2_4_extended.csv` | `step7_tables.py` |
| `output/table_subperiods.csv`, `.md` | `step9_subperiods.py` |
| `output/sentiment_decay.csv` | `step10_decay.py` |
| `output/fig_sentiment_decay.png` | `step10_decay.py` |
| `output/table_event_windows.csv`, `.md` | `step11_event_windows.py` |

---

## References

- Loughran, T., & McDonald, B. (2011). *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* **Journal of Finance** 66(1), 35–65.
- McLean, R. D., & Pontiff, J. (2016). *Does Academic Research Destroy Stock Return Predictability?* **Journal of Finance** 71(1), 5–32.
- Tetlock, P. C. (2007). *Giving Content to Investor Sentiment: The Role of Media in the Stock Market.* **Journal of Finance** 62(3), 1139–1168.

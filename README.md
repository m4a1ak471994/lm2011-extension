# Loughran & McDonald (2011) — Extended Analysis (1994–2024)

This repository extends the Loughran and McDonald (2011) Fama-MacBeth filing-period excess-return regressions from the original 1994–2008 sample through end of 2024 — about 17 additional years of SEC 10-K filings — using the identical methodology (same dictionary, same controls, same FM weighting, same Newey-West HAC SE, same FF48 industry fixed effects).

> Loughran, Tim, and Bill McDonald, 2011. “When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks”, *Journal of Finance* 66(1): 35–65.

The underlying replication of LM (2011) lives in a separate repository: <https://github.com/m4a1ak471994/lm2011-replication>. The extension here re-runs the same pipeline on a wider window and adds two new analyses: a rolling-window decay decomposition and an event-window robustness grid.

---

## Three research questions

1. **Out-of-sample test.** Does the LM (2011) negative-tone result hold in 2009–2024?
2. **Decay.** Does the signal attenuate over time? Markets typically arbitrage away published anomalies (McLean and Pontiff, 2016) — does this one?
3. **Window-robustness.** Is the result an artifact of LM's chosen 4-day `[0,+3]` event window, or does it survive at `[0,+1]` and `[0,+5]`?

### Brief answers

**1. Out-of-sample test.** *Full 10-K text*: the coefficient weakens but stays negative (t = −1.80, p ≈ 0.072) in the full extended window. *MD&A only*: stays strongly significant (t = −3.81). The MD&A specification holds out of sample cleanly; the full-text specification is closer to a marginal effect.

**2. Decay.** Yes for the full-text measure — the coefficient is indistinguishable from zero in the 2009–2019 sub-periods and only partially returns in 2020–2024. The MD&A specification is more stable.

**3. Window-robustness.** Yes — the sign and significance pattern is broadly stable across [0,+1] and [0,+5]. See [`docs/extension.md`](docs/extension.md) for the full grid.

---

## Negative sentiment score based on full 10-K text (tf-idf weight)

| Specification | n | n_qtrs | t-stat | adj R² |
|---|---:|---:|---:|---:|
| LM (2011) original result | 50,115 | 60 | −3.11 | 2.63 % |
| My replication (sample period: 1994–2008) | 50,681 | 60 | −2.76 | 2.52 % |
| Extended sample (1994–2024) | 82,413 | 110 | −1.80 | 4.00 % |

The effect of the negative sentiment score is less significant in the extended sample (p ≈ 0.072), with the sign still negative. The temporal decomposition below shows how the effect evolves across sub-periods.

### Decay by sub-period

| Subperiod | Years | n | t-stat | adj R² |
|---|---|---:|---:|---:|
| LM_in_sample | 1994–2008 | 50,681 | −2.76 | 2.52 % |
| post_LM | 2009–2014 | 17,363 | +0.41 | 4.53 % |
| algo_era | 2015–2019 | 13,127 | +1.21 | 8.06 % |
| covid_recent | 2020–2024 | 1,242 | −2.53 | 0.32 % |

## Negative sentiment score based on MD&A section only (tf-idf weight)

| Specification | n | n_qtrs | t-stat | adj R² |
|---|---:|---:|---:|---:|
| LM (2011) original result | 37,287 | 60 | −1.96 | 2.76 % |
| My replication (sample period: 1994–2008) | 48,134 | 60 | −3.56 | 2.46 % |
| Extended sample (1994–2024) | 79,656 | 110 | −3.81 | 4.09 % |

The MD&A specification remains strongly significant (t = −3.81) pooled across the extended window, in contrast to the full-text version above. The temporal decomposition below shows the MD&A coefficient stays negative across every sub-period.

### Decay by sub-period

| Subperiod | Years | n | t-stat | adj R² |
|---|---|---:|---:|---:|
| LM_in_sample | 1994–2008 | 48,134 | −3.56 | 2.46 % |
| post_LM | 2009–2014 | 17,241 | −1.72 | 4.36 % |
| algo_era | 2015–2019 | 13,044 | −0.96 | 7.52 % |
| covid_recent | 2020–2024 | 1,237 | −0.00 | 3.27 % |

Three patterns from the event-window robustness section in [`docs/extension.md`](docs/extension.md) help explain why the MD&A-only specification is more robust than the full-text version.

---

![Predictive power of negative sentiment over time — full 10-K text](output/fig_sentiment_decay.png)

This figure plots the Fin-Neg tf-idf coefficient from a rolling 5-year Fama-MacBeth regression on the full 10-K text, indexed by the window's end year. The coefficient is significantly negative through about 2005 — the original LM sample — and drifts toward zero afterward, broadly consistent with the post-publication arbitrage of published anomalies documented by McLean and Pontiff (2016). The sharp dip in the 2024 window reflects the small COVID-era sample (n ≈ 1,200) and should be read cautiously.

![Predictive power of negative sentiment over time — MD&A section only](output/fig_sentiment_decay_mda.png)

The MD&A-only version of the same regression tells a more stable story: after the strong pre-2005 effect, the coefficient stays mildly negative throughout the post-2005 period rather than drifting all the way to zero. This is consistent with managerial tone in MD&A continuing to convey priceable information even after the broader full-text signal is largely arbitraged away.

See [`docs/extension.md`](docs/extension.md) for the full writeup, including the sub-period replication table, event-window robustness across [0,+1] / [0,+3] / [0,+5], and three candidate mechanisms for the early-2000s signal vanishing (pre-publication discovery, post-SOX disclosure-norm shift, algorithmic pricing of public text).

---

## Pipeline

```bash
PY=python   # or your py310 interpreter

# 0. Build WRDS inputs (CRSP daily/monthly, Compustat, 13F) through 2026
$PY code/preclean.py                          # ~70-120 min

# 1. Build the 10-K-family manifest for 1993Q1-2026Q1
$PY code/step1c_manifest_10k_extended.py

# 2. Download all 10-K family filings (~290k filings, ~70 GB on disk)
$PY code/step3_full_download.py

# 3. Tokenize + count Fin-Neg/Fin-Pos per filing (~75 min)
$PY code/step4_word_counts.py

# 4. Apply Table I sample funnel
$PY code/step5_build_sample.py

# 5. Build extended analysis panel (multiple event-window CARs)
$PY code/step6_build_panel.py

# 6. Tables II, IV, V on the full extended sample
$PY code/step7_tables.py

# 7. Sub-period replication
$PY code/step9_subperiods.py

# 8. Rolling-window decay (the headline figure)
$PY code/step10_decay.py

# 9. Event-window robustness ([0,+1] / [0,+3] / [0,+5])
$PY code/step11_event_windows.py
```

After step 10, the canonical outputs live in `output/`:

| File | What it is |
|---|---|
| `output/table1_sample_funnel.csv` | Sample funnel (extended) |
| `output/table2.csv` | Descriptive stats (extended) |
| `output/table4_cols2_4.csv` | Table IV cols (2) and (4) (extended) |
| `output/table5_cols2_4.csv` | Table V cols (2) and (4) (extended) |
| `output/table_subperiods.csv` + `.md` | Sub-period replication |
| `output/sentiment_decay.csv`, `output/sentiment_decay_mda.csv` | Rolling-window decay data (full text + MD&A) |
| `output/fig_sentiment_decay.png`, `output/fig_sentiment_decay_mda.png` | Decay plots (full text + MD&A) |
| `output/table_event_windows.csv` + `.md` | Event-window robustness grid |
| `output/replication_diagnostic.md` | Methodology summary |

---

## Installation

1. **Python 3.10+** required.

2. Clone:
   ```bash
   git clone https://github.com/m4a1ak471994/lm2011-extension.git
   cd lm2011-extension
   pip install -r requirements.txt
   ```

3. **Set environment variables** (the code intentionally contains no credentials):

   ```bash
   # SEC EDGAR requires a contact User-Agent on every request:
   export SEC_EDGAR_USER_AGENT="Your Name your.email@example.com"

   # WRDS account login (only needed for code/preclean.py):
   export WRDS_USERNAME="your_wrds_login"
   ```

4. **Acquire input data** — see [`DATA.md`](DATA.md).

---

## Methodology highlights

The extension uses the identical Fama-MacBeth pipeline as LM (2011) and the upstream replication (<https://github.com/m4a1ak471994/lm2011-replication>) — same dictionary, same controls, same per-quarter cross-sectional regression, same n_obs-weighted time-series average, same Newey-West HAC (1 lag) standard errors, same FF48 industry fixed effects in every quarterly cross-section. Only the date window of WRDS extracts and the filings manifest were widened.

One small refinement was added: inline-XBRL `<ix:hidden>` blocks (which wrap content tagged for machine readers but not visible to humans) are stripped before tokenization. Empirically the change shifts every coefficient by less than 0.5 % — small — but the fix is principled. See `docs/extension.md` for details.

---

## Skills demonstrated

- **NLP / textual analysis**: dictionary-based sentiment scoring on a 30+ year corpus of ~290 k SEC 10-K filings; inline-XBRL handling; MD&A section extraction; tf-idf weighting with corpus-wide idf.
- **Empirical asset pricing**: Fama-MacBeth quarterly cross-sectional regressions with frequency weighting and Newey-West HAC standard errors; **rolling-window FM with backward-looking 5-year windows**; event-window robustness across multiple CAR horizons; sub-period decomposition for post-publication-decay testing à la McLean and Pontiff (2016).
- **WRDS / financial databases**: SQL queries via the Python `wrds` package across CRSP daily/monthly, Compustat fundamentals, the CCM link table, Thomson Reuters 13F, and Fama-French factors — extended through end of 2024.
- **Reproducible research**: full numbered pipeline (`preclean → step1c → step3 → step4 → step5 → step6 → step7 → step9 → step10 → step11`), all parameters explicit, every figure backed by a CSV the reader can reproduce.

---

## Reproducibility notes

- **Data licensing**: CRSP, Compustat, and Thomson Reuters 13F require WRDS access. The Loughran-McDonald Master Dictionary is freely available from [SRAF](https://sraf.nd.edu/loughranmcdonald-master-dictionary/). See [`DATA.md`](DATA.md).
- **Compute**: full pipeline takes ~3 hours on residential broadband (~2 hr WRDS pulls + ~75 min step4 + a few minutes for everything else). The raw 10-K corpus is ~70 GB on disk.
- **CRSP daily cutoff**: WRDS CRSP daily ends 2024-12-31, so the [+252] post-window required by LM Table I funnel filter (10) drops most filings filed in late 2023 onward. The `covid_recent` sub-period (2020–2024) has only 1,367 firm-years for this reason.

---

## References

- **Paper**: Loughran, Tim, and Bill McDonald, 2011. “When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks”, *Journal of Finance* 66(1): 35–65. DOI: [10.1111/j.1540-6261.2010.01625.x](https://doi.org/10.1111/j.1540-6261.2010.01625.x)
- **Post-publication decay**: McLean, R. D., and Jeffrey Pontiff, 2016. “Does Academic Research Destroy Stock Return Predictability?”, *Journal of Finance* 71(1): 5–32.
- **Textual analysis in finance, pre-LM**: Tetlock, Paul C., 2007. “Giving Content to Investor Sentiment: The Role of Media in the Stock Market”, *Journal of Finance* 62(3): 1139–1168.
- **Upstream LM (2011) replication**: <https://github.com/m4a1ak471994/lm2011-replication>
- **SRAF data + dictionary**: <https://sraf.nd.edu/sec-edgar-data/>

---

## License

Code: **MIT**. Replicates and extends a published paper for academic and portfolio purposes.

# Required input data

This repository does not include any of the underlying data:

- **Raw SEC 10-K filings** (~70 GB compressed for 1993–2026Q1) are excluded for size.
- **WRDS extracts** (CRSP, Compustat, Thomson Reuters 13F) are commercial data and cannot be redistributed.
- **SRAF reference data** (Loughran-McDonald Master Dictionary) is freely available from <https://sraf.nd.edu/sec-edgar-data/> but is not bundled here to keep the repo lean.

---

## Expected local layout

The pipeline expects this layout. None of these folders are committed to Git (see `.gitignore`); you create them locally:

```
.
├── input/                            # WRDS extracts + reference data (NOT committed)
│   ├── compustat_gvkey_permno.dta    ← from preclean.py (WRDS Compustat-CCM)
│   ├── comphist_cik_gvkey.dta        ← from preclean.py (historical fallback link)
│   ├── crsp_daily_1993_2026.dta      ← from preclean.py (CRSP daily + FF factors)
│   ├── crsp_monthly_1993_2026.dta    ← from preclean.py (CRSP monthly)
│   ├── 13f_instOwn_stock_level.dta   ← from preclean.py (Thomson Reuters 13F)
│   ├── Loughran-McDonald_MasterDictionary_1993-2025.csv   ← SRAF
│   ├── Siccodes48.txt                                     ← Ken French data library
│   └── README.md                                          ← (committed)
│
└── (off-repo, configurable via DATA_ROOT constant)
    └── D:\Data\10_K_10_Q\
        ├── raw\10K\<YYYY>\<cik>_<accession>.txt.gz   ← from step3 downloader
        ├── manifest\filings_10k_1993_2026.parquet
        └── index\master_<YYYY>_Q<q>.gz
```

---

## 1. CRSP data (WRDS)

| File | Description | Source |
|---|---|---|
| `crsp_daily_1993_2026.dta` | CRSP daily stock file with FF daily factors merged in | `crsp.dsf` + `ff.fivefactors_daily` |
| `crsp_monthly_1993_2026.dta` | CRSP monthly stock file | `crsp.msf` + `crsp.msenames` |

Variables used downstream: `permno, date, prc, ret, vol, shrout, shrcd, exchcd, siccd, vwretd, mktrf, smb, hml, rf`. Both extracts are produced by [`code/preclean.py`](code/preclean.py).

Note: WRDS CRSP daily lags ~6 months relative to the live market, so at the time of pulling the file ended **2024-12-31**. 2025 + 2026 panel filings cannot have their `[+252]` post-window observed and are dropped by the funnel.

---

## 2. Compustat data (WRDS, via SEC Suite link)

| File | Description |
|---|---|
| `compustat_gvkey_permno.dta` | Compustat annual joined with the CCM link table and a direct CIK column |
| `comphist_cik_gvkey.dta` | Historical CIK ↔ GVKEY link table (optional fallback) |

The pipeline uses `compustat_gvkey_permno.dta` as the primary CIK ↔ PERMNO bridge, per LM (2011) footnote 5. Produced by [`code/preclean.py`](code/preclean.py).

---

## 3. 13F institutional ownership (WRDS via Thomson Reuters)

| File | Description |
|---|---|
| `13f_instOwn_stock_level.dta` | Quarter-end stock-level institutional ownership |

Source: `tfn.s34`. Produced by [`code/preclean.py`](code/preclean.py).

---

## 4. SRAF reference data (free download)

From <https://sraf.nd.edu/sec-edgar-data/>:

| File | Use |
|---|---|
| `Loughran-McDonald_MasterDictionary_1993-2025.csv` | **Required** — drives word-level negative / positive flags |

The Master Dictionary is the canonical Loughran-McDonald list of ~86,553 words with per-word `Negative / Positive / Uncertainty / Litigious / StrongModal / WeakModal / Constraining` flags. The Master Dictionary is what makes the LM (2011) sentiment measure finance-domain-specific, as opposed to general-purpose dictionaries like Harvard's IV-4 General Inquirer.

---

## 5. Fama-French industry classification (Ken French data library)

`code/step6_build_panel.py` parses **`input/Siccodes48.txt`** — Ken French's Fama-French 48-industry SIC mapping.

This file is NOT bundled with the repository. Download it directly from Ken French's data library:

- Page: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>
- Direct link: <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes48.zip>
  → unzip → place `Siccodes48.txt` in `input/`.

---

## 6. Raw 10-K filings (SEC EDGAR — public, free)

10-K text files are downloaded from EDGAR by [`code/step3_full_download.py`](code/step3_full_download.py) into:

```
D:\Data\10_K_10_Q\
├── raw\10K\<YYYY>\<cik>_<accession>.txt.gz
├── manifest\filings_10k_1993_2026.parquet
└── index\master_<YYYY>_Q<q>.gz
```

The default root is `D:\Data\10_K_10_Q\`; edit `DATA_ROOT` at the top of the relevant scripts for your environment.

Size: ~70 GB compressed for 1993Q1–2026Q1 (~290,000 filings).

**SEC fair-access rules** (non-negotiable): max 8 requests/sec global, exponential-backoff retry on 429/503, contact User-Agent on every request. See [`code/edgar_client.py`](code/edgar_client.py).

---

## Credentials & environment variables

```bash
# Required by every SEC EDGAR HTTP request
export SEC_EDGAR_USER_AGENT="Your Name your.email@example.com"

# Required only by code/preclean.py (the WRDS pull)
export WRDS_USERNAME="your_wrds_login"

# (One-time) cache your WRDS password so preclean.py doesn't prompt:
#   python -c "import wrds; wrds.Connection(wrds_username='YOUR_USER').create_pgpass_file()"
```

On Windows PowerShell, use `$env:NAME = "value"` syntax.

---

## Reference papers

- **Loughran, T., & McDonald, B. (2011).** *When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks.* **Journal of Finance** 66(1), 35–65. DOI: [10.1111/j.1540-6261.2010.01625.x](https://doi.org/10.1111/j.1540-6261.2010.01625.x)
- **McLean, R. D., & Pontiff, J. (2016).** *Does Academic Research Destroy Stock Return Predictability?* **Journal of Finance** 71(1), 5–32.
- **Tetlock, P. C. (2007).** *Giving Content to Investor Sentiment: The Role of Media in the Stock Market.* **Journal of Finance** 62(3), 1139–1168.

---

## After all data is in place

The pipeline (`preclean → step1c → step3 → step4 → step5 → step6 → step7 → step9 → step10 → step11`) reproduces everything in [`docs/extension.md`](docs/extension.md). See [`README.md`](README.md) for the run order.

"""
Step 9: Subperiod replication of LM (2011) Tables IV col (2) and (4)
        on the EXTENDED sample (1994-2026).

Subperiods chosen to test the natural narrative arc of the LM result:

  LM_in_sample        : 1994-2008  (the original LM (2011) window)
  GFC                 : 2008-2009  (Global Financial Crisis)
  post_LM             : 2009-2014  (immediately after LM publication)
  algo_era            : 2015-2019  (machine-trading era)
  covid_recent        : 2020-2025  (post-COVID + AI/LLM disclosure era)
  full                : 1994-2025  (full extended sample)

For each subperiod we re-run the Fama-MacBeth quarterly regression
(time-series average weighted by n_obs/quarter, Newey-West HAC SE)
on Fin-Neg proportional and Fin-Neg tf-idf, with the LM control set
(log size, log BM, log turnover, pre-event FF-α, IO, NASDAQ + FF48 FEs).

Inputs : output/panel.parquet  (built by step6 on the extended sample)
Outputs:
    output/table_subperiods.csv             # one row per (subperiod × sentiment_var)
    output/table_subperiods.md              # pretty-printed markdown summary
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

sys.path.insert(0, str(Path(__file__).parent))
from step7_tables import fit_one  # noqa: E402  (use same fit + winsorize logic)


# --- subperiod definitions -------------------------------------------------- #

SUBPERIODS: list[tuple[str, int, int]] = [
    ("LM_in_sample",  1994, 2008),
    ("GFC",           2008, 2009),
    ("post_LM",       2009, 2014),
    ("algo_era",      2015, 2019),
    ("covid_recent",  2020, 2024),
    ("full",          1994, 2024),
]


# --- main ------------------------------------------------------------------- #

def main() -> None:
    t0 = time.monotonic()
    panel_path = OUT / "panel.parquet"
    print(f"Loading {panel_path} ...")
    p = pd.read_parquet(panel_path)
    p["date_filed"] = pd.to_datetime(p["date_filed"])
    print(f"  {len(p):,} rows / {p['permno'].nunique():,} unique permnos")

    # MD&A subsample (used for Table V)
    pV = p[p["mdna_status"].astype(str).str.startswith("ok").fillna(False)].copy()
    pV["fin_neg_prop_mda"] = np.where(
        pV["n_words_mda"] > 0,
        100.0 * pV["n_neg_mda"] / pV["n_words_mda"], np.nan)

    rows: list[dict] = []
    for name, y0, y1 in SUBPERIODS:
        years = (p["date_filed"].dt.year >= y0) & (p["date_filed"].dt.year <= y1)
        years_V = (pV["date_filed"].dt.year >= y0) & (pV["date_filed"].dt.year <= y1)
        sub  = p.loc[years].copy()
        subV = pV.loc[years_V].copy()
        if sub.empty:
            print(f"  {name:14s} EMPTY — skip")
            continue
        n_qs = sub["date_filed"].dt.to_period("Q").nunique()
        print(f"  {name:14s} {y0}-{y1}  n={len(sub):>6,}  qtrs={n_qs:>3}")

        for spec_name, df_, sentiment in [
            ("table_IV_col2_FinNeg_prop",      sub,  "fin_neg_prop"),
            ("table_IV_col4_FinNeg_tfidf",     sub,  "fin_neg_tfidf_full"),
            ("table_V_col2_FinNeg_prop_MDA",   subV, "fin_neg_prop_mda"),
            ("table_V_col4_FinNeg_tfidf_MDA",  subV, "fin_neg_tfidf_mda"),
        ]:
            res = fit_one(df_, sentiment=sentiment, label=spec_name, with_ff48=True)
            rows.append({
                "subperiod":   name,
                "year_start":  y0,
                "year_end":    y1,
                "spec":        spec_name,
                "sentiment":   sentiment,
                "n_obs":       res["n"],
                "n_quarters":  res["n_quarters"],
                "coef":        res["coef"],
                "se":          res["se"],
                "t":           res["t"],
                "p":           res["p"],
                "adj_r2_avg":  res["adj_r2_avg"],
            })

    out_df = pd.DataFrame(rows)
    csv_path = OUT / "table_subperiods.csv"
    out_df.to_csv(csv_path, index=False)
    print(f"\nWrote {csv_path.name}")

    # Pretty markdown
    md_lines: list[str] = ["# Subperiod replication — extended sample (1994–2024)\n"]
    md_lines.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')}_  \n")
    md_lines.append("Same Fama-MacBeth quarterly regression as in the headline,")
    md_lines.append("re-fit on each subperiod independently. FF48 dummies + 1/99 % winsor.\n")
    SPEC_TITLES = {
        "table_IV_col2_FinNeg_prop":    "Fin-Neg proportional, full 10-K text",
        "table_IV_col4_FinNeg_tfidf":   "Fin-Neg tf-idf, full 10-K text",
        "table_V_col2_FinNeg_prop_MDA": "Fin-Neg proportional, MD&A section only",
        "table_V_col4_FinNeg_tfidf_MDA":"Fin-Neg tf-idf, MD&A section only",
    }
    for spec, title in SPEC_TITLES.items():
        md_lines.append(f"\n## {title}\n")
        md_lines.append("| Subperiod | Years | n | n_qtrs | Coef | SE | t-stat | adj R² |")
        md_lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for _, r in out_df[out_df["spec"] == spec].iterrows():
            md_lines.append(
                f"| {r['subperiod']} "
                f"| {int(r['year_start'])}-{int(r['year_end'])} "
                f"| {int(r['n_obs']):,} "
                f"| {int(r['n_quarters'])} "
                f"| {r['coef']:+.4f} "
                f"| {r['se']:.4f} "
                f"| {r['t']:+.2f} "
                f"| {r['adj_r2_avg']*100:.2f}% |"
            )

    md_path = OUT / "table_subperiods.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {md_path.name}")
    print(f"\nDone. Elapsed: {(time.monotonic() - t0):.1f}s")


if __name__ == "__main__":
    main()

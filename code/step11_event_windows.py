"""
Step 11: Event-window robustness for LM (2011) Tables IV col (2) and (4).

For each of five trading-day post-filing windows {[0,+1], [0,+3], [0,+5],
[0,+10], [0,+20]}, re-fit the same Fama-MacBeth quarterly regression of
filing-period excess return on Fin-Neg (proportional and tf-idf) with the LM
control set (log size, log BM, log turnover, FF-α pre, IO, NASDAQ + FF48 FEs).

The question this section answers: is the LM (2011) [0,+3] result an artifact
of the specific 4-day window LM chose, or does it generalize across short and
longer post-filing horizons?

Inputs : output/panel.parquet  (must have excret_01, excret_03, excret_05,
                                excret_10, excret_20 columns from step6)
Outputs:
    output/table_event_windows.csv   # one row per (window × spec × subperiod)
    output/table_event_windows.md    # pretty markdown summary
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
from step7_tables import fama_macbeth_quarterly  # noqa: E402


EVENT_WINDOWS = [
    ("excret_01", "[0,+1]"),
    ("excret_03", "[0,+3]"),   # LM canonical
    ("excret_05", "[0,+5]"),
    # [0,+10] and [0,+20] were dropped from reporting — too long for an
    # information-event excess-return analysis: at horizons of 2–4 weeks the
    # LHS is contaminated by drift, earnings surprises (other firms),
    # and macroeconomic news unrelated to the 10-K release.
]

# Same subperiods as step9
SUBPERIODS: list[tuple[str, int, int]] = [
    ("LM_in_sample",  1994, 2008),
    ("post_LM",       2009, 2014),
    ("algo_era",      2015, 2019),
    ("covid_recent",  2020, 2024),
    ("full",          1994, 2024),
]

CONTROLS = ["log_size", "log_bm", "log_turnover", "ff_alpha_pre", "nasdaq", "io"]


def fit(d: pd.DataFrame, y: str, x_main: str) -> dict:
    res = fama_macbeth_quarterly(
        d, y=y, x_main=x_main, controls=CONTROLS, industry_col="ff48")
    return res


def main() -> None:
    t0 = time.monotonic()
    p = pd.read_parquet(OUT / "panel.parquet")
    p["date_filed"] = pd.to_datetime(p["date_filed"])
    print(f"Loaded panel.parquet  rows={len(p):,}  years {int(p['date_filed'].dt.year.min())}..{int(p['date_filed'].dt.year.max())}")

    # MD&A subsample (Table V col 4 only — for compactness)
    pV = p[p["mdna_status"].astype(str).str.startswith("ok").fillna(False)].copy()
    pV["fin_neg_prop_mda"] = np.where(
        pV["n_words_mda"] > 0,
        100.0 * pV["n_neg_mda"] / pV["n_words_mda"], np.nan)

    # Specifications to run: full-text col 2, full-text col 4, MD&A col 2 + col 4.
    SPECS = [
        ("IV_col2_prop",      "fin_neg_prop",       p,  "full"),
        ("IV_col4_tfidf",     "fin_neg_tfidf_full", p,  "full"),
        ("V_col2_prop_MDA",   "fin_neg_prop_mda",   pV, "MDA"),
        ("V_col4_tfidf_MDA",  "fin_neg_tfidf_mda",  pV, "MDA"),
    ]

    rows: list[dict] = []
    for spec_name, x_main, df_, doc in SPECS:
        for sub_name, y0, y1 in SUBPERIODS:
            mask = (df_["date_filed"].dt.year >= y0) & (df_["date_filed"].dt.year <= y1)
            sub = df_.loc[mask].copy()
            if sub.empty:
                continue
            for excret_col, lbl in EVENT_WINDOWS:
                if excret_col not in sub.columns:
                    continue
                res = fit(sub, y=excret_col, x_main=x_main)
                rows.append({
                    "spec":         spec_name,
                    "doc_scope":    doc,
                    "subperiod":    sub_name,
                    "year_start":   y0,
                    "year_end":     y1,
                    "event_window": lbl,
                    "y":            excret_col,
                    "n_obs":        res["n"],
                    "n_quarters":   res["n_quarters"],
                    "coef":         res["coef"],
                    "se":           res["se"],
                    "t":            res["t"],
                    "p":            res["p"],
                    "adj_r2_avg":   res["adj_r2_avg"],
                })
                print(f"  {spec_name:18s} {sub_name:14s} {lbl:10s}  "
                      f"n={res['n']:>6,}  coef={res['coef']:+.5f}  "
                      f"t={res['t']:+.2f}  adj_R2={res['adj_r2_avg']*100:.2f}%")

    out_df = pd.DataFrame(rows)
    csv_path = OUT / "table_event_windows.csv"
    out_df.to_csv(csv_path, index=False)
    print(f"\nWrote {csv_path.name}")

    # Pretty markdown: one section per spec, table = subperiod × event_window
    md_lines: list[str] = ["# Event-window robustness — extended sample (1994–2024)\n"]
    md_lines.append(f"_Generated {time.strftime('%Y-%m-%d %H:%M:%S')}_  \n")
    md_lines.append("Same Fama-MacBeth quarterly regression as in the headline,")
    md_lines.append("re-fit for three LHS event-windows. Each cell shows `t-stat (adj R²)`.")
    md_lines.append("The [0,+3] column is LM's canonical 4-day filing-period window.\n")

    SPEC_TITLES = {
        "IV_col2_prop":     "Fin-Neg proportional, full 10-K text",
        "IV_col4_tfidf":    "Fin-Neg tf-idf, full 10-K text",
        "V_col2_prop_MDA":  "Fin-Neg proportional, MD&A section only",
        "V_col4_tfidf_MDA": "Fin-Neg tf-idf, MD&A section only",
    }
    for spec_name, x_main, df_, doc in SPECS:
        md_lines.append(f"\n## {SPEC_TITLES.get(spec_name, spec_name)}\n")
        sub_df = out_df[out_df["spec"] == spec_name]
        if sub_df.empty:
            md_lines.append("_no rows_")
            continue
        header = "| Subperiod (n_qtrs) | n (canonical) | " + " | ".join(w for _, w in EVENT_WINDOWS) + " |"
        sep    = "|---|---:|" + "---:|" * len(EVENT_WINDOWS)
        md_lines.append(header)
        md_lines.append(sep)
        for sub_name, y0, y1 in SUBPERIODS:
            sub_rows = sub_df[sub_df["subperiod"] == sub_name]
            if sub_rows.empty:
                continue
            n_canon = int(sub_rows.iloc[0]["n_obs"])
            n_q = int(sub_rows.iloc[0]["n_quarters"])
            cells = []
            for excret_col, _ in EVENT_WINDOWS:
                r = sub_rows[sub_rows["y"] == excret_col]
                if r.empty:
                    cells.append("–")
                    continue
                r = r.iloc[0]
                cells.append(f"{r['t']:+.2f} ({r['adj_r2_avg']*100:.2f}%)")
            md_lines.append(f"| {sub_name} ({n_q}q) | {n_canon:,} | " + " | ".join(cells) + " |")

    md_path = OUT / "table_event_windows.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Wrote {md_path.name}")
    print(f"\nDone. Elapsed: {(time.monotonic() - t0):.1f}s")


if __name__ == "__main__":
    main()

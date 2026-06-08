"""
Step 10: Rolling-window Fama-MacBeth on Fin-Neg over the extended sample.

For each end year t in [yr_min + WINDOW_LEN − 1, yr_max], re-fit the
filing-period excess-return regression on a 5-year trailing window of
filings filed in [t − 4, t]. Plot the Fin-Neg coefficient (and its 95 % CI)
over time.

Two parallel specifications are run:
  - fin_neg_tfidf_full : negative sentiment computed on the full 10-K text
  - fin_neg_tfidf_mda  : negative sentiment computed on the MD&A section only

Inputs : output/panel.parquet (built by step6 on extended sample)
Outputs:
    output/sentiment_decay.csv               # full-text rolling-window stats
    output/sentiment_decay_mda.csv           # MD&A rolling-window stats
    output/fig_sentiment_decay.png           # full-text decay plot
    output/fig_sentiment_decay_mda.png       # MD&A decay plot
"""
from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

sys.path.insert(0, str(Path(__file__).parent))
from step7_tables import fit_one  # noqa: E402

# Rolling-window parameters
WINDOW_LEN = 5            # 5-year trailing window
YEAR_START_GLOBAL = 1994  # drop pre-1994 filings entirely (LM's own window start)

# Two specifications to plot — full 10-K text and MD&A-only.
SPECS = [
    {
        "sentiment_var": "fin_neg_tfidf_full",
        "scope":         "Full 10-K text",
        "mdna_only":     False,
        "csv_name":      "sentiment_decay.csv",
        "png_name":      "fig_sentiment_decay.png",
    },
    {
        "sentiment_var": "fin_neg_tfidf_mda",
        "scope":         "MD&A section only",
        "mdna_only":     True,
        "csv_name":      "sentiment_decay_mda.csv",
        "png_name":      "fig_sentiment_decay_mda.png",
    },
]


def run_spec(p_full: pd.DataFrame, spec: dict) -> None:
    print(f"\n=== {spec['scope']} ({spec['sentiment_var']}) ===")
    p = p_full.copy()
    if spec["mdna_only"]:
        p = p[p["mdna_status"].astype(str).str.startswith("ok").fillna(False)].copy()
        print(f"  After MD&A-ok filter: {len(p):,} rows")

    yr_min, yr_max = int(p["year"].min()), int(p["year"].max())
    end_years = list(range(yr_min + WINDOW_LEN - 1, yr_max + 1))
    print(f"  Running {len(end_years)} rolling FM regressions "
          f"({WINDOW_LEN}-yr trailing window, indexed by end year)")

    rows: list[dict] = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for ye in end_years:
            ys = ye - WINDOW_LEN + 1
            sub = p[(p["year"] >= ys) & (p["year"] <= ye)].copy()
            if sub.empty:
                continue
            res = fit_one(sub, sentiment=spec["sentiment_var"],
                          label=f"window_end_{ye}", with_ff48=True)
            ci_lo = res["coef"] - 1.96 * res["se"] if res["se"] else np.nan
            ci_hi = res["coef"] + 1.96 * res["se"] if res["se"] else np.nan
            rows.append({
                "year_end":    ye,
                "year_start":  ys,
                "n_obs":       res["n"],
                "n_quarters":  res["n_quarters"],
                "coef":        res["coef"],
                "se":          res["se"],
                "t":           res["t"],
                "p":           res["p"],
                "adj_r2_avg":  res["adj_r2_avg"],
                "ci_lo":       ci_lo,
                "ci_hi":       ci_hi,
            })
            print(f"    end={ye} ({ys}-{ye})  n={res['n']:>6,}  "
                  f"coef={res['coef']:+.4f}  t={res['t']:+.2f}  "
                  f"adj_R2={res['adj_r2_avg']*100:.2f}%")

    out_df = pd.DataFrame(rows)
    csv_path = OUT / spec["csv_name"]
    out_df.to_csv(csv_path, index=False)
    print(f"  Wrote {csv_path.name}")

    # --- Plot ---
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.fill_between(out_df["year_end"], out_df["ci_lo"], out_df["ci_hi"],
                        alpha=0.18, color="steelblue", label="95 % CI")
        ax.plot(out_df["year_end"], out_df["coef"],
                marker="o", linewidth=1.6, color="steelblue",
                label=f"Fin-Neg coefficient ({WINDOW_LEN}-yr trailing window)")
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.6)
        ax.axvline(2011, color="red", linewidth=0.7, linestyle=":", alpha=0.7)
        ax.text(2011.2, ax.get_ylim()[1] * 0.92, "LM (2011) published",
                color="red", fontsize=9, va="top")

        ax.set_xlabel(f"Window end year (window = end_year − {WINDOW_LEN-1} to end_year)")
        ax.set_ylabel("Fin-Neg tf-idf coefficient on excess return [0,+3] (%)")
        ax.set_title(
            f"Predictive power of negative sentiment over time "
            f"({WINDOW_LEN}-year rolling window)\n{spec['scope']}"
        )
        # Show every calendar year on the x-axis at 45° rotation
        years = out_df["year_end"].tolist()
        ax.set_xticks(years)
        ax.set_xticklabels(years, rotation=45, ha="right")
        ax.grid(True, alpha=0.25)
        ax.legend(loc="lower right", framealpha=0.92)
        plt.tight_layout()
        png_path = OUT / spec["png_name"]
        plt.savefig(png_path, dpi=150)
        print(f"  Wrote {png_path.name}")
        plt.close(fig)
    except ImportError:
        print("  matplotlib not available — skipping figure")


def main() -> None:
    t0 = time.monotonic()
    panel_path = OUT / "panel.parquet"
    print(f"Loading {panel_path} ...")
    p = pd.read_parquet(panel_path)
    p["date_filed"] = pd.to_datetime(p["date_filed"])
    p["year"] = p["date_filed"].dt.year
    p = p[p["year"] >= YEAR_START_GLOBAL].copy()
    print(f"  {len(p):,} rows after dropping pre-{YEAR_START_GLOBAL}  "
          f"(years {int(p['year'].min())}..{int(p['year'].max())})")

    for spec in SPECS:
        run_spec(p, spec)

    print(f"\nDone. Elapsed: {(time.monotonic() - t0):.1f}s")


if __name__ == "__main__":
    main()

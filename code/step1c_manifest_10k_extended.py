"""
Step 1c: Build the 10-K-family filing manifest for the EXTENDED window
(1993 Q1 .. 2026 Q1).

Mirrors step1_manifest.py exactly except:
  - Window extended: 1993Q1 .. 2026Q1 (vs LM's 1994Q1..2008Q4).
  - 10-K family ONLY (no 10-Qs — those are for a separate analysis).

Output: D:\\Data\\10_K_10_Q\\manifest\\filings_10k_1993_2026.parquet
"""

from __future__ import annotations

import gzip
import io
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from edgar_client import download_to_gzip  # noqa: E402

ROOT = Path(r"D:\lm2011-extension")
DATA_ROOT = Path(r"D:\Data\10_K_10_Q")
IDX_DIR = DATA_ROOT / "index"
MAN_DIR = DATA_ROOT / "manifest"
for d in (IDX_DIR, MAN_DIR):
    d.mkdir(parents=True, exist_ok=True)

MANIFEST_PATH = MAN_DIR / "filings_10k_1993_2026.parquet"

F_10K = {"10-K", "10-K405", "10KSB", "10-KSB", "10KSB40"}
F_10KA = {"10-K/A", "10-K405/A", "10KSB/A", "10-KSB/A", "10KSB40/A"}
F_10KT = {"10-KT", "10KT405", "10-KT/A", "10KT405/A"}
FORM_TO_FAMILY: dict[str, str] = (
    {f: "10K" for f in F_10K}
    | {f: "10KA" for f in F_10KA}
    | {f: "10KT" for f in F_10KT}
)

START_YEAR = 1993
END_YEAR = 2026
END_QUARTER = 1  # only Q1 of END_YEAR

ACC_RE = re.compile(r"(\d{10}-\d{2}-\d{6})")


def _quarters() -> list[tuple[int, int]]:
    qs: list[tuple[int, int]] = []
    for y in range(START_YEAR, END_YEAR + 1):
        last_q = END_QUARTER if y == END_YEAR else 4
        for q in range(1, last_q + 1):
            qs.append((y, q))
    return qs


def fetch_indexes() -> list[Path]:
    """Download all master.gz files we don't already have. Return local paths."""
    paths: list[Path] = []
    for y, q in _quarters():
        url = f"https://www.sec.gov/Archives/edgar/full-index/{y}/QTR{q}/master.gz"
        dest = IDX_DIR / f"master_{y}_Q{q}.gz"
        paths.append(dest)
        if dest.exists() and dest.stat().st_size > 0:
            continue
        print(f"  fetch {y}Q{q} ... ", end="", flush=True)
        status, n, dt = download_to_gzip(url, dest)
        print(f"{status}  {n/1024:,.0f} KB  {dt:.1f}s")
    return paths


def parse_one(path: Path) -> pd.DataFrame:
    """Parse one master.gz into a DataFrame of 10-K-family rows."""
    with gzip.open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("latin-1", errors="replace")
    lines = text.splitlines()
    start = 0
    for i, ln in enumerate(lines):
        if ln.count("|") == 4 and ln.split("|")[0].strip().isdigit():
            start = i
            break
    body = "\n".join(lines[start:])
    df = pd.read_csv(
        io.StringIO(body),
        sep="|",
        header=None,
        names=["cik", "company_name", "form_type", "date_filed", "filename"],
        dtype={"cik": "Int64", "company_name": str, "form_type": str,
               "date_filed": str, "filename": str},
        engine="c",
    )
    df = df.dropna(subset=["cik", "form_type", "filename"])
    df["form_type"] = df["form_type"].str.strip()
    df = df[df["form_type"].isin(FORM_TO_FAMILY)].copy()
    if df.empty:
        return df
    df["form_family"] = df["form_type"].map(FORM_TO_FAMILY)
    df["filename"] = df["filename"].str.strip()
    df = df[df["filename"].str.endswith(".txt")].copy()
    df["accession"] = df["filename"].str.extract(ACC_RE, expand=False)
    df = df.dropna(subset=["accession"]).copy()
    df["date_filed"] = pd.to_datetime(df["date_filed"], errors="coerce").dt.date
    df = df.dropna(subset=["date_filed"]).copy()
    df["txt_url"] = "https://www.sec.gov/Archives/" + df["filename"]
    df["cik"] = df["cik"].astype("int64")
    return df[["cik", "company_name", "accession", "form_type",
               "form_family", "date_filed", "txt_url"]]


def main() -> None:
    qs = _quarters()
    print(f"Step 1c: fetching quarterly indexes "
          f"({qs[0][0]}Q{qs[0][1]}..{qs[-1][0]}Q{qs[-1][1]}, {len(qs)} quarters) ...")
    idx_paths = fetch_indexes()
    print(f"Have {len(idx_paths)} index files.")

    print("Parsing ...")
    frames: list[pd.DataFrame] = []
    for p in idx_paths:
        df = parse_one(p)
        if not df.empty:
            frames.append(df)
    big = pd.concat(frames, ignore_index=True)
    print(f"Raw 10-K-family rows: {len(big):,}")

    before = len(big)
    big = big.drop_duplicates(subset=["cik", "accession"], keep="first").reset_index(drop=True)
    print(f"After dedupe on (cik, accession): {len(big):,}  (dropped {before - len(big):,})")

    big["status"] = "pending"
    big = big[["cik", "company_name", "accession", "form_type",
               "form_family", "date_filed", "txt_url", "status"]]
    big.to_parquet(MANIFEST_PATH, index=False)
    print(f"Wrote manifest -> {MANIFEST_PATH}")

    big["year"] = pd.to_datetime(big["date_filed"]).dt.year
    tab = big.groupby(["year", "form_family"]).size().unstack(fill_value=0)
    for c in ["10K", "10KA", "10KT"]:
        if c not in tab.columns:
            tab[c] = 0
    tab = tab[["10K", "10KA", "10KT"]]
    tab["TOTAL"] = tab.sum(axis=1)
    print("\nRow counts by year x form_family:")
    print(tab.to_string())
    print(f"\nGRAND TOTAL: {len(big):,}")

    uniq = big.drop_duplicates(subset=["accession"])
    print(f"Unique accessions: {len(uniq):,}")


if __name__ == "__main__":
    main()

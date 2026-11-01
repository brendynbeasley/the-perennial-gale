"""Extension: are positions of market power temporary, as Schumpeter said?

Schumpeter argued that a monopoly position "is in general no cushion to sleep on" and that the
"perennial gale of creative destruction" wears concentrated positions down. This script asks how
much of an industry's 2002 concentration was still there twenty years later.

  1. Four-firm concentration (CR4) for 2002 and 2022 from the Economic Census.
  2. Keeps only six-digit manufacturing industries whose definition did not change in any of the
     four NAICS revisions in between (2007, 2012, 2017, 2022): the code maps one-to-one onto
     itself in every Census concordance.
  3. Regresses CR4 in 2022 on CR4 in 2002, tests persistence = 1, and converts the slope into a
     half-life; tabulates how industries moved between concentration bands.

Inputs (committed in data/raw/):
    EC0231SR12.dat, EC2200SIZECONCEN.dat       2002 and 2022 concentration tables
    2002_to_2007_NAICS.xls, 2007_to_2012_NAICS.xls, 2012_to_2017_NAICS.xlsx, 2017_to_2022_NAICS.xlsx
Writes:
    results/persistence.csv, results/persistence_transitions.csv,
    results/persistence_industries.csv, results/persistence_named.csv, results/persistence.png

Usage (from the repository root, after src/schumpeter_test.py):
    python src/temporary_monopoly.py
"""

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats as sstats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

YEARS = 20                          # 2002 to 2022
BANDS = [0, 25, 50, 75, 100.01]     # CR4 bands for the transition table, in percent
BAND_LABELS = ["Under 25%", "25-50%", "50-75%", "75% or more"]
HIGH_CR4 = 50                       # same split as src/schumpeter_test.py
CONCORDANCES = ["2002_to_2007_NAICS.xls", "2007_to_2012_NAICS.xls",
                "2012_to_2017_NAICS.xlsx", "2017_to_2022_NAICS.xlsx"]

# Same naming convention as src/schumpeter_test.py: well-known producers, not Census data.
NAMED = {
    312221: "Philip Morris (Altria), R.J. Reynolds",
    331312: "Alcoa, Century Aluminum",
    336411: "Boeing",
    311230: "Kellogg, General Mills, Post, Quaker",
    334111: "Dell, Hewlett-Packard, Apple",
    312120: "Anheuser-Busch, Miller, Coors",
    334413: "Intel, Texas Instruments, Micron",
    325412: "Pfizer, Merck, Johnson & Johnson",
    331111: "U.S. Steel, Nucor",
    324110: "ExxonMobil, ConocoPhillips, BP",
    327320: "Thousands of local producers",
}


def unchanged_codes():
    """Six-digit manufacturing codes that map one-to-one onto themselves in every revision."""
    keep = None
    for f in CONCORDANCES:
        engine = "openpyxl" if f.endswith(".xlsx") else "xlrd"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")   # pandas notes a future change of default Excel engine
            d = pd.read_excel(RAW / f, header=2, engine=engine).iloc[:, [0, 2]]
        d.columns = ["src", "dst"]
        d = d.dropna()
        d = d[d.src.astype(str).str.match(r"^3[1-3]\d{4}$")].astype(int)
        n_src, n_dst = d.groupby("src").size(), d.groupby("dst").size()
        same = d[(d.src == d.dst) & d.src.map(n_src).eq(1) & d.dst.map(n_dst).eq(1)]
        print(f"  {f}: {d.src.nunique()} manufacturing codes, {len(same)} unchanged")
        keep = set(same.src) if keep is None else keep & set(same.src)
    print(f"Unchanged in all four revisions: {len(keep)} codes")
    return keep


def load_2002():
    e = pd.read_csv(RAW / "EC0231SR12.dat", sep="|", dtype=str)
    e.columns = [c.strip() for c in e.columns]
    e = e[e.NAICS2002.str.len() == 6].copy()
    e.loc[e.CCORCPPCT_F.str.strip() == "D", "CCORCPPCT"] = np.nan
    allc = e[e.CONCENFI == "004"].set_index("NAICS2002")
    out = pd.DataFrame({"title": allc.NAICS2002_MEANING,
                        "companies_2002": pd.to_numeric(allc.COMPANY, errors="coerce"),
                        "cr4_2002": pd.to_numeric(e[e.CONCENFI == "856"].set_index("NAICS2002").CCORCPPCT,
                                                  errors="coerce")})
    out.index = out.index.astype(int)
    return out


def load_2022():
    z = pd.read_csv(RAW / "EC2200SIZECONCEN.dat", sep="|", dtype=str)
    z.columns = [c.lstrip("#") for c in z.columns]
    z = z[(z.SECTOR == "31") & (z.NAICS2022.str.len() == 6)].copy()
    z.loc[z.VAL_PCT_F.fillna("").str.strip() == "D", "VAL_PCT"] = np.nan
    allf = z[z.CONCENFI == "001"].set_index("NAICS2022")
    out = pd.DataFrame({"title_2022": allf.NAICS2022_LABEL,
                        "companies_2022": pd.to_numeric(allf.FIRM, errors="coerce"),
                        "shipments_2022_k": pd.to_numeric(allf.RCPTOT, errors="coerce"),
                        "cr4_2022": pd.to_numeric(z[z.CONCENFI == "604"].set_index("NAICS2022").VAL_PCT,
                                                  errors="coerce")})
    out.index = out.index.astype(int)
    return out


def main():
    OUT.mkdir(exist_ok=True)
    c02, c22 = load_2002(), load_2022()
    print(f"Loaded 2002 concentration: {len(c02)} industries; 2022: {len(c22)} industries")
    keep = unchanged_codes()
    df = c02.join(c22, how="inner")
    print(f"Codes present in both years: {len(df)}")
    df = df[df.index.isin(keep)]
    print(f"Kept {len(df)} with an unchanged definition")
    before = len(df)
    df = df.dropna(subset=["cr4_2002", "cr4_2022"])
    print(f"Dropped {before - len(df)} with a suppressed CR4 in either year; kept {len(df)}")
    df["change"] = df.cr4_2022 - df.cr4_2002
    df.index.name = "naics"
    df.to_csv(OUT / "persistence_industries.csv", float_format="%.2f")

    groups = pd.factorize(df.index // 100)[0]
    m = smf.ols("cr4_2022 ~ cr4_2002", df).fit(cov_type="cluster", cov_kwds={"groups": groups})
    rho, se = m.params["cr4_2002"], m.bse["cr4_2002"]
    t_one = (rho - 1) / se
    p_one = 2 * (1 - sstats.norm.cdf(abs(t_one)))
    lo, hi = m.conf_int().loc["cr4_2002"]
    annual = rho ** (1 / YEARS)
    half_life = np.log(0.5) / np.log(annual)
    hi_set = df[df.cr4_2002 >= HIGH_CR4]
    stats = {
        "industries": len(df), "rho": rho, "rho_se": se, "rho_ci_lo": lo, "rho_ci_hi": hi,
        "t_rho_eq_1": t_one, "p_rho_eq_1": p_one, "intercept": m.params["Intercept"], "r2": m.rsquared,
        "annual_persistence": annual, "half_life_years": half_life,
        "half_life_ci_lo": YEARS * np.log(0.5) / np.log(lo), "half_life_ci_hi": YEARS * np.log(0.5) / np.log(hi),
        "long_run_mean": m.params["Intercept"] / (1 - rho),
        "mean_2002": df.cr4_2002.mean(), "mean_2022": df.cr4_2022.mean(),
        "sd_2002": df.cr4_2002.std(), "sd_2022": df.cr4_2022.std(),
        "corr": df[["cr4_2002", "cr4_2022"]].corr().iloc[0, 1],
        "rank_corr": df[["cr4_2002", "cr4_2022"]].corr(method="spearman").iloc[0, 1],
        "high_n_2002": len(hi_set), "high_still_high": int((hi_set.cr4_2022 >= HIGH_CR4).sum()),
        "high_share_still_high": (hi_set.cr4_2022 >= HIGH_CR4).mean(),
        "high_mean_change": hi_set.change.mean(),
        "low_mean_change": df[df.cr4_2002 < HIGH_CR4].change.mean(),
        "low_n_2002": int((df.cr4_2002 < HIGH_CR4).sum()),
        "low_became_high": int(((df.cr4_2002 < HIGH_CR4) & (df.cr4_2022 >= HIGH_CR4)).sum()),
        "abs_change_mean": df.change.abs().mean(),
        "share_moved_10_points": (df.change.abs() >= 10).mean(),
    }
    pd.DataFrame([stats]).T.rename(columns={0: "value"}).to_csv(OUT / "persistence.csv", float_format="%.4f")
    print("\nPersistence of CR4, 2002 to 2022:")
    for k, v in stats.items():
        print(f"  {k:24s} {v:10.3f}")

    df["band_2002"] = pd.cut(df.cr4_2002, BANDS, labels=BAND_LABELS, right=False)
    df["band_2022"] = pd.cut(df.cr4_2022, BANDS, labels=BAND_LABELS, right=False)
    tr = pd.crosstab(df.band_2002, df.band_2022)
    tr.to_csv(OUT / "persistence_transitions.csv")
    print("\nIndustries by CR4 band, 2002 (rows) and 2022 (columns):")
    print(tr.to_string())

    rows = []
    for code, leaders in NAMED.items():
        if code in df.index:
            r = df.loc[code]
            rows.append({"naics": code, "title": r.title, "leaders_2002": leaders,
                         "cr4_2002": r.cr4_2002, "cr4_2022": r.cr4_2022, "change": r.change,
                         "companies_2002": int(r.companies_2002), "companies_2022": int(r.companies_2022)})
        else:
            print(f"  named industry {code} not in the unchanged sample, skipped")
    pd.DataFrame(rows).sort_values("cr4_2002", ascending=False).to_csv(
        OUT / "persistence_named.csv", index=False, float_format="%.1f")

    fig, ax = plt.subplots(figsize=(6.4, 6))
    ax.scatter(df.cr4_2002, df.cr4_2022, s=18, alpha=0.55, color="#3b6ea5", edgecolor="white", linewidth=0.4)
    xs = np.linspace(0, 100, 50)
    ax.plot(xs, xs, color="grey", lw=0.8, ls="--", label="No change (45-degree line)")
    ax.plot(xs, m.params["Intercept"] + rho * xs, color="black", lw=1.2,
            label=f"Fitted: CR4 2022 = {m.params['Intercept']:.1f} + {rho:.2f} x CR4 2002")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Four-firm share of shipments, 2002 (%)")
    ax.set_ylabel("Four-firm share of shipments, 2022 (%)")
    ax.set_title(f"{len(df)} manufacturing industries with unchanged definitions", fontsize=11)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "persistence.png", dpi=150)
    plt.close(fig)
    print("\nWrote persistence results to results/")


if __name__ == "__main__":
    main()

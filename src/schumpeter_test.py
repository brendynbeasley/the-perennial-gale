"""Schumpeter (1942) on modern data: did the industries run by a few big firms make things cheaper?

In chapters 7 and 8 of Capitalism, Socialism and Democracy, Schumpeter argued that the large
concern is "the most powerful engine" of progress. His own yardstick was the price of goods in
hours of work (each year's money price divided by each year's hourly wage) and the long-run
growth of output, and he said the items where progress was greatest led "to the doors of the
large concerns." This script turns that into a cross-industry test on US manufacturing.

  1. Concentration in 2002 for every 6-digit NAICS manufacturing industry, from the 2002
     Economic Census (CR4, CR8, HHI of the 50 largest firms, number of companies).
  2. Industry outcomes from 2002 to 2016 from the NBER-CES Manufacturing Industry Database:
     the price of the industry's output in hours of manufacturing labor, real output, and
     five-factor total factor productivity (TFP). 2016 is the last year with TFP.
  3. Quintile table, regressions of each outcome on initial CR4 (unweighted, value-added
     weighted, with 3-digit subsector fixed effects, and several robustness versions),
     standard errors clustered by 4-digit industry group.
  4. A table of named industries and two figures.

Inputs (committed in data/raw/):
    nberces5818v1_n1997.csv   NBER-CES database, NAICS 1997 codes, 1958-2018
    EC0231SR12.dat            2002 Economic Census, manufacturing concentration ratios
    EC0731SR12.dat            2007 Economic Census, same table (robustness window)
Writes:
    results/industries.csv, results/quintiles.csv, results/regressions.csv,
    results/named_industries.csv, results/headline.csv, results/manufacturing_wage.csv,
    results/price_in_hours.png, results/tfp_by_quintile.png

Usage (from the repository root):
    python src/schumpeter_test.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

START, END = 2002, 2016      # Census year; last NBER-CES year with TFP (capital stock ends 2016)
ALT_START = 2007             # second Census year, for a shorter robustness window
WINSOR = (0.01, 0.99)        # trimming for the winsorized robustness run only
Y_FLOOR = -19                # lower edge of the price figure, % per year
HIGH_CR4 = 50                # "four firms with half the market", the split used in the summary table
# NBER-CES shipment price indexes that fall far faster than the industry's own materials price index in
# 2015-2016 (log change 2014-2016 at least 0.39 below materials): refining and petrochemicals. A check, not a rule.
PRICE_BREAKS = [324110, 325110]

# Industries named in the README. The Census does not name companies; the leaders listed are the
# industry's well-known producers in the early 2000s, as in the Bain repository's named table.
NAMED = {
    334111: "Dell, Hewlett-Packard, Apple",
    334413: "Intel, Texas Instruments, Micron",
    331312: "Alcoa, Century Aluminum",
    312221: "Philip Morris (Altria), R.J. Reynolds",
    311230: "Kellogg, General Mills, Post, Quaker",
    336411: "Boeing",
    336111: "General Motors, Ford, DaimlerChrysler, Toyota",
    312120: "Anheuser-Busch, Miller, Coors",
    325412: "Pfizer, Merck, Johnson & Johnson",
    335221: "Whirlpool, GE, Electrolux",
    331111: "U.S. Steel, Nucor",
    324110: "ExxonMobil, ConocoPhillips, BP",
    327320: "Thousands of local producers",
    332710: "Thousands of machine shops",
    323110: "Thousands of print shops",
    321113: "Weyerhaeuser and thousands of small mills",
}


def load_concentration(path, year):
    """National CR4, CR8, HHI and company counts for 6-digit manufacturing industries."""
    e = pd.read_csv(path, sep="|", dtype=str)
    e.columns = [c.strip() for c in e.columns]
    code = f"NAICS{year}"
    e = e[e[code].str.len() == 6].copy()
    for col in ["CCORCPPCT", "VSHERFI"]:               # "D" = withheld to avoid disclosing a company
        e.loc[e[col + "_F"].str.strip() == "D", col] = np.nan
    num = lambda s: pd.to_numeric(s, errors="coerce")
    allc = e[e.CONCENFI == "004"].set_index(code)
    out = pd.DataFrame({
        "title": allc[f"{code}_MEANING"],
        "companies": num(allc.COMPANY),
        "shipments_k": num(allc.RCPTOT),
        "hhi": num(e[e.CONCENFI == "859"].set_index(code).VSHERFI).replace(0, np.nan),
        "cr4": num(e[e.CONCENFI == "856"].set_index(code).CCORCPPCT),
        "cr8": num(e[e.CONCENFI == "857"].set_index(code).CCORCPPCT),
    })
    out.index = out.index.astype(int)
    out.index.name = "naics"
    print(f"Loaded {path.name}: {len(out)} six-digit industries, CR4 published for {out.cr4.notna().sum()}")
    return out


def growth(df, col, t0, t1):
    """Annualized log change, in percent per year."""
    return 100 * (np.log(df[f"{col}_{t1}"]) - np.log(df[f"{col}_{t0}"])) / (t1 - t0)


def build_panel():
    ces = pd.read_csv(RAW / "nberces5818v1_n1997.csv")
    print(f"Loaded NBER-CES: {len(ces):,} industry-years, {ces.naics.nunique()} industries, "
          f"{ces.year.min()}-{ces.year.max()}")
    # The hourly wage of a manufacturing production worker: total production-worker pay over hours.
    wage = ces.groupby("year")[["prodw", "prodh"]].sum()
    wage["wage"] = wage.prodw / wage.prodh
    wage[["wage"]].reset_index().to_csv(OUT / "manufacturing_wage.csv", index=False)

    ces = ces.merge(wage[["wage"]], left_on="year", right_index=True)
    ces["hours_price"] = ces.piship / ces.wage          # price index in hours of labor
    ces["real_output"] = ces.vship / ces.piship
    ces["pcm"] = 100 * (ces.vadd - ces.pay) / ces.vship  # price-cost margin, % of shipments
    keep = ["vship", "vadd", "emp", "piship", "hours_price", "real_output", "tfp5", "pcm"]
    wide = ces[ces.year.isin([START, ALT_START, END])].pivot(index="naics", columns="year", values=keep)
    wide.columns = [f"{v}_{y}" for v, y in wide.columns]

    c02 = load_concentration(RAW / "EC0231SR12.dat", START)
    c07 = load_concentration(RAW / "EC0731SR12.dat", ALT_START)[["cr4"]].rename(columns={"cr4": "cr4_2007"})
    df = c02.join(wide, how="inner").join(c07, how="left")
    print(f"Matched {len(df)} industries between the 2002 Census and NBER-CES "
          f"(of {len(c02)} Census and {len(wide)} NBER-CES industries)")

    for col, name in [("hours_price", "g_hours_price"), ("real_output", "g_output"),
                      ("tfp5", "g_tfp"), ("piship", "g_price")]:
        df[name] = growth(df, col, START, END)
        df[name + "_07"] = growth(df, col, ALT_START, END)
    df["d_pcm"] = df[f"pcm_{END}"] - df[f"pcm_{START}"]          # change in points, not annualized
    df["d_pcm_07"] = df[f"pcm_{END}"] - df[f"pcm_{ALT_START}"]
    df["sub3"] = (df.index // 1000).astype(str)
    df["grp4"] = (df.index // 100).astype(str)
    df["size"] = np.log(df.shipments_k / df.companies)      # log average company size, $1,000
    df["w_va"] = df[f"vadd_{START}"]

    before = len(df)
    df = df[df.cr4.notna()]
    print(f"Dropped {before - len(df)} industries with suppressed 2002 CR4; kept {len(df)}")
    bad = ~np.isfinite(df[["g_hours_price", "g_output", "g_tfp"]]).all(axis=1)
    df = df[~bad]
    print(f"Dropped {bad.sum()} industries with a zero or missing outcome; kept {len(df)}")
    return df, wage


def fit(df, y, x="cr4", weights=None, fe=False):
    d = df.dropna(subset=[y, x]).copy()
    d["xs"] = d[x] / 10 if x.startswith("cr") else d[x]
    formula = f"{y} ~ xs" + (" + C(sub3)" if fe else "")
    groups = pd.factorize(d.grp4)[0]
    if weights == "median":
        m = smf.quantreg(formula, d).fit(q=0.5)
        lo, hi = m.conf_int().loc["xs"]
        return {"b": m.params["xs"], "se": m.bse["xs"], "p": m.pvalues["xs"], "ci_lo": lo, "ci_hi": hi,
                "n": int(m.nobs), "clusters": np.nan, "r2": m.prsquared}
    if weights is None:
        m = smf.ols(formula, d).fit(cov_type="cluster", cov_kwds={"groups": groups})
    else:
        m = smf.wls(formula, d, weights=d[weights]).fit(cov_type="cluster", cov_kwds={"groups": groups})
    lo, hi = m.conf_int().loc["xs"]
    return {"b": m.params["xs"], "se": m.bse["xs"], "p": m.pvalues["xs"], "ci_lo": lo, "ci_hi": hi,
            "n": int(m.nobs), "clusters": len(set(groups)), "r2": m.rsquared}


def winsorize(s):
    lo, hi = s.quantile(WINSOR[0]), s.quantile(WINSOR[1])
    return s.clip(lo, hi)


def regressions(df):
    outcomes = {"g_hours_price": "Price in hours of labor", "g_output": "Real output",
                "g_tfp": "Total factor productivity", "d_pcm": "Price-cost margin change (points)"}
    w = df.copy()
    for y in outcomes:
        w[y] = winsorize(w[y])
    no334 = df[df.sub3 != "334"]
    nobreak = df.drop(index=[c for c in PRICE_BREAKS if c in df.index])
    specs = [
        ("Unweighted", df, "cr4", None, False),
        ("Value-added weighted", df, "cr4", "w_va", False),
        ("Subsector fixed effects", df, "cr4", None, True),
        ("Without computers and electronics (334)", no334, "cr4", None, False),
        ("Without 334 and value-added weighted", no334, "cr4", "w_va", False),
        ("Winsorized 1%/99%", w, "cr4", None, False),
        ("Without refining and petrochemicals (324110, 325110)", nobreak, "cr4", None, False),
        ("CR8 instead of CR4", df, "cr8", None, False),
        ("HHI per 1000 instead of CR4", df.assign(hhi_k=df.hhi / 1000), "hhi_k", None, False),
        ("Median regression", df, "cr4", "median", False),
        ("Log average company size", df, "size", None, False),
        ("Log average company size with subsector FE", df, "size", None, True),
    ]
    rows = []
    for y, label in outcomes.items():
        for name, d, x, wt, fe in specs:
            rows.append({"outcome": label, "spec": name, "window": f"{START}-{END}", **fit(d, y, x, wt, fe)})
        d7 = df.dropna(subset=["cr4_2007"]).assign(cr4=lambda t: t.cr4_2007)
        rows.append({"outcome": label, "spec": "2007 CR4 with 2007-2016 growth", "window": f"{ALT_START}-{END}",
                     **fit(d7, y + "_07", "cr4", None, False)})
    reg = pd.DataFrame(rows)
    reg.to_csv(OUT / "regressions.csv", index=False, float_format="%.4f")
    main = reg[reg.spec.isin(["Unweighted", "Value-added weighted", "Subsector fixed effects",
                              "Without computers and electronics (334)"])]
    print("\nSlope per 10 points of 2002 CR4 (percent per year), clustered SE:")
    print(main[["outcome", "spec", "b", "se", "p", "n"]].round(3).to_string(index=False))
    return reg


def wmean(d, col, w):
    return np.average(d[col], weights=d[w])


def quintiles(df):
    d = df.copy()
    d["quintile"] = pd.qcut(d.cr4, 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rows = []
    for q, g in d.groupby("quintile"):
        rows.append({"quintile": q, "industries": len(g), "cr4_min": g.cr4.min(), "cr4_max": g.cr4.max(),
                     "cr4_mean": g.cr4.mean(), "value_added_2002_bn": g.w_va.sum() / 1000,
                     "g_hours_price": g.g_hours_price.mean(), "g_output": g.g_output.mean(),
                     "g_tfp": g.g_tfp.mean(), "g_hours_price_vaw": wmean(g, "g_hours_price", "w_va"),
                     "g_output_vaw": wmean(g, "g_output", "w_va"), "g_tfp_vaw": wmean(g, "g_tfp", "w_va"),
                     "g_tfp_median": g.g_tfp.median(), "d_pcm": g.d_pcm.mean(),
                     "pcm_2002": g.pcm_2002.mean(), "g_hours_price_median": g.g_hours_price.median()})
    q = pd.DataFrame(rows)
    q.to_csv(OUT / "quintiles.csv", index=False, float_format="%.3f")
    print("\nOutcomes by 2002 CR4 quintile (unweighted means, percent per year):")
    print(q[["quintile", "industries", "cr4_min", "cr4_max", "g_hours_price", "g_output", "g_tfp"]]
          .round(2).to_string(index=False))
    return d


def headline(df, wage):
    hi, lo = df[df.cr4 >= HIGH_CR4], df[df.cr4 < HIGH_CR4]
    rows = []
    for col in ["g_hours_price", "g_output", "g_tfp", "d_pcm"]:
        t = stats.ttest_ind(hi[col], lo[col], equal_var=False)
        rows.append({"measure": col, "high_n": len(hi), "low_n": len(lo), "high_mean": hi[col].mean(),
                     "low_mean": lo[col].mean(), "gap": hi[col].mean() - lo[col].mean(),
                     "welch_t": t.statistic, "p": t.pvalue,
                     "high_vaw": wmean(hi, col, "w_va"), "low_vaw": wmean(lo, col, "w_va")})
    h = pd.DataFrame(rows)
    extra = pd.DataFrame([
        {"measure": "wage_2002", "high_mean": wage.loc[START, "wage"]},
        {"measure": "wage_2016", "high_mean": wage.loc[END, "wage"]},
        {"measure": "industries", "high_mean": len(df)},
        {"measure": "share_value_added_high_cr4", "high_mean": hi.w_va.sum() / df.w_va.sum()},
        {"measure": "all_mfg_g_hours_price_vaw", "high_mean": wmean(df, "g_hours_price", "w_va")},
        {"measure": "all_mfg_g_tfp_vaw", "high_mean": wmean(df, "g_tfp", "w_va")},
        {"measure": "corr_g_tfp_g_hours_price", "high_mean": df[["g_tfp", "g_hours_price"]].corr().iloc[0, 1]},
    ])
    q = pd.read_csv(OUT / "quintiles.csv")
    gap = q.g_tfp.iloc[-1] - q.g_tfp.iloc[0]
    years = END - START
    extra = pd.concat([extra, pd.DataFrame([
        {"measure": "tfp_gap_q5_minus_q1_per_year", "high_mean": gap},
        {"measure": "tfp_gap_q5_minus_q1_cumulative_pct", "high_mean": 100 * (np.exp(gap * years / 100) - 1)},
        {"measure": "tfp_gap_high_minus_low_cumulative_pct",
         "high_mean": 100 * (np.exp(rows[2]["gap"] * years / 100) - 1)},
    ])], ignore_index=True)
    h = pd.concat([h, extra], ignore_index=True)
    h.to_csv(OUT / "headline.csv", index=False, float_format="%.4f")
    print(f"\nCR4 >= {HIGH_CR4}: {len(hi)} industries; below: {len(lo)}")
    print(h.round(3).to_string(index=False))


def named(df):
    rows = []
    for code, leaders in NAMED.items():
        if code not in df.index:
            print(f"  named industry {code} not in sample, skipped")
            continue
        r = df.loc[code]
        rows.append({"naics": code, "title": r.title, "leaders": leaders, "companies_2002": int(r.companies),
                     "cr4_2002": r.cr4, "shipments_2002_bn": r.shipments_k / 1e6,
                     "hours_price_change_pct": 100 * (r[f"hours_price_{END}"] / r[f"hours_price_{START}"] - 1),
                     "g_hours_price": r.g_hours_price, "g_output": r.g_output, "g_tfp": r.g_tfp,
                     "pcm_2002": r.pcm_2002, "d_pcm": r.d_pcm,
                     "tfp_change_pct": 100 * (r[f"tfp5_{END}"] / r[f"tfp5_{START}"] - 1),
                     "real_output_change_pct": 100 * (r[f"real_output_{END}"] / r[f"real_output_{START}"] - 1)})
    t = pd.DataFrame(rows).sort_values("cr4_2002", ascending=False)
    t.to_csv(OUT / "named_industries.csv", index=False, float_format="%.2f")
    print("\nNamed industries:")
    print(t[["naics", "title", "cr4_2002", "g_hours_price", "g_output", "g_tfp"]].round(2).to_string(index=False))


def figures(df, reg):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    size = 8 + 250 * df.w_va / df.w_va.max()
    is334 = df.sub3 == "334"
    ax.scatter(df.cr4[~is334], df.g_hours_price[~is334], s=size[~is334], alpha=0.45, color="#3b6ea5",
               edgecolor="white", linewidth=0.4, label="Other manufacturing")
    ax.scatter(df.cr4[is334], df.g_hours_price[is334], s=size[is334], alpha=0.65, color="#c8553d",
               edgecolor="white", linewidth=0.4, label="Computers and electronics (NAICS 334)")
    r = reg[(reg.outcome == "Price in hours of labor") & (reg.spec == "Unweighted")].iloc[0]
    a = df.g_hours_price.mean() - r.b * df.cr4.mean() / 10
    xs = np.linspace(0, 100, 50)
    ax.plot(xs, a + r.b * xs / 10, color="black", lw=1.2, label=f"OLS slope {r.b:+.2f} per 10 points of CR4")
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_ylim(Y_FLOOR, 6)
    ax.set_xlabel("Share of shipments made by the four largest companies, 2002 (CR4, %)")
    ax.set_ylabel("Change in price measured in hours of labor,\n2002-2016 (% per year, log)")
    ax.set_title("Price of each industry's output in hours of factory work", fontsize=11)
    ax.legend(fontsize=8, loc="lower left", frameon=False)
    clipped = (df.g_hours_price < Y_FLOOR).sum()
    if clipped:
        ax.text(99, Y_FLOOR + 1, f"{clipped} industry below the axis not shown", ha="right", fontsize=7, color="grey")
    fig.tight_layout()
    fig.savefig(OUT / "price_in_hours.png", dpi=150)
    plt.close(fig)

    q = pd.read_csv(OUT / "quintiles.csv")
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    x = np.arange(len(q))
    ax.bar(x - 0.2, q.g_tfp, width=0.4, color="#3b6ea5", label="Mean industry")
    ax.bar(x + 0.2, q.g_tfp_median, width=0.4, color="#9bb7d4", label="Median industry")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Q{int(r.quintile)}\nCR4 {r.cr4_min:.0f}-{r.cr4_max:.0f}%" for r in q.itertuples()])
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_ylabel("TFP growth, 2002-2016 (% per year)")
    ax.set_title("Productivity growth by 2002 concentration quintile", fontsize=11)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "tfp_by_quintile.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    df, wage = build_panel()
    reg = regressions(df)
    quintiles(df)
    headline(df, wage)
    named(df)
    cols = ["title", "companies", "shipments_k", "cr4", "cr8", "hhi", "cr4_2007", "vadd_2002",
            "piship_2002", "piship_2016", "hours_price_2002", "hours_price_2016", "tfp5_2002", "tfp5_2016", "pcm_2002", "pcm_2016", "g_hours_price",
            "g_output", "g_tfp", "g_price", "d_pcm"]
    df[cols].to_csv(OUT / "industries.csv", float_format="%.4f")
    figures(df, reg)
    print(f"\nWrote results for {len(df)} industries to results/")


if __name__ == "__main__":
    main()

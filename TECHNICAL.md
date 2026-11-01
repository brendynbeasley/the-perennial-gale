# Technical notes

This is the technical companion to the [README](README.md). It covers the original study, the data, the rules,
every test statistic and how to reproduce the results. Every table is in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Joseph A. Schumpeter, *Capitalism, Socialism and Democracy*, New York: Harper & Brothers, 1942, chapters 7 ("The
Process of Creative Destruction") and 8 ("Monopolistic Practices"). The book is an argument, not an econometric
study. Its central empirical claims are that the largest price reductions in hours of labor since the 1890s came
from industries dominated by large concerns, that the large-scale firm is "the most powerful engine" of the long-run
expansion of output, and that monopoly positions are eroded by the competition of new goods and methods. Its one
worked case (chapter 8, footnote 20, p. 101 of the second edition) is the Aluminum Company of America: from 1890 to
1929 the price of aluminum fell to about 12% of its 1890 level, or about 8.8% deflated by the BLS wholesale price
index, while output rose from 30 to 103,400 metric tons. Chapter 5 (p. 64) reports US total production growth of
3.7% a year from 1870 to 1930 on the Day-Persons index, 4.3% for manufactures.

## Headline results

| Test | Estimate | SE | 95% CI | p | N |
|---|---|---|---|---|---|
| TFP growth on CR4/10, 2002-2016 | +0.121 | 0.054 | [0.015, 0.226] | 0.025 | 471 |
| Price in hours of labor on CR4/10 | -0.090 | 0.052 | [-0.192, 0.013] | 0.087 | 471 |
| Real output growth on CR4/10 | -0.052 | 0.141 | [-0.328, 0.224] | 0.712 | 471 |
| Price-cost margin change on CR4/10 | -0.062 | 0.227 | [-0.506, 0.382] | 0.785 | 471 |
| Persistence of CR4, 2002 to 2022 | 0.840 | 0.035 | [0.770, 0.909] | < 0.001 for ρ = 1 | 256 |

Growth outcomes are in percent a year; the margin change is in percentage points over 2002-2016. Slopes are per 10
points of CR4. The most concentrated fifth of industries (CR4 61.9-99.2%) had TFP growth of 0.77% a year against
0.12% for the least concentrated fifth (CR4 2.2-23.8%). The persistence slope implies a half-life of 79 years for a
departure from the long-run mean. The TFP slope falls to 0.107 (p = 0.055) without refining and petrochemicals,
whose price indexes break in 2015-2016.

## Data

All inputs are committed in `data/raw/` and were downloaded on 1 November 2026.

| File | Source | Use |
|---|---|---|
| `nberces5818v1_n1997.csv` | NBER-CES Manufacturing Industry Database, version 2021a, NAICS 1997 codes, `data.nber.org/nberces/nberces5818v1/` | Shipments, value added, payroll, production-worker hours and wages, shipment price index, five-factor TFP |
| `EC0231SR12.dat` | 2002 Economic Census, concentration by largest companies, manufacturing, `www2.census.gov/programs-surveys/economic-census/data/2002/sector31/` | CR4, CR8, HHI, company counts |
| `EC0731SR12.dat` | Same table for 2007, `.../data/2007/sector31/` | Robustness window |
| `EC2200SIZECONCEN.dat` | 2022 Economic Census, concentration by largest firms, `.../data/2022/sector00/` | CR4 in 2022 |
| `2002_to_2007_NAICS.xls` ... `2017_to_2022_NAICS.xlsx` | Census NAICS concordances, `www.census.gov/naics/concordances/` | Industries with unchanged definitions |

The 2002 Census uses NAICS 2002 codes and the NBER-CES file NAICS 1997 codes; all 473 six-digit manufacturing
codes in the Census table appear in the NBER-CES file, and every NBER-CES industry appears in the Census table.

## Method

Rules fixed before looking at results:

- **Sample:** all six-digit manufacturing industries in both the 2002 Census and NBER-CES. Industries whose CR4 is
  withheld ("D" flag) are dropped (2 of 473).
- **Window:** 2002 concentration, outcomes from 2002 to 2016. 2016 is the last NBER-CES year with a capital stock
  and therefore with TFP. The 2007 Census gives a second window, 2007-2016;
  its CR4 is matched by code, and 17 codes had small boundary changes between NAICS 2002 and 2007.
- **Price in hours of labor:** the shipment price index divided by the all-manufacturing production-worker hourly
  wage (total production-worker pay over total production-worker hours). Because the wage is common to all
  industries, it shifts the level of this outcome but not the cross-industry slope.
- **Price-cost margin:** (value added − payroll) / shipments, in percent.
- **Inference:** standard errors clustered by four-digit NAICS group (86 clusters); Welch t-test for the CR4 ≥ 50
  split; the median regression uses its own asymptotic standard errors.
- **Persistence sample:** codes that map one to one onto themselves in each of the four concordances (257), of which
  one has a withheld CR4 in 2022.
- **Check added after the first results:** NBER-CES shipment price indexes for petroleum refining (324110) and
  petrochemicals (325110) fall far faster than their materials price indexes in 2015-2016 (log change 2014-2016
  more than 0.39 below materials, against at most 0.30 for every other industry), inflating measured output and
  TFP. Both stay in the main sample; one specification drops them.

The outcomes are annualized log changes,

```math
g^{x}_j = \frac{100}{T}\left(\ln x_{j,2016} - \ln x_{j,2002}\right), \qquad x \in \{H,\ Q,\ A\},\quad T = 14
```

with $`H = p/\bar{w}`$ the price in hours of labor, $`Q`$ real shipments and $`A`$ five-factor TFP. The reason the
price and productivity outcomes are linked is the dual identity under constant returns, Hicks-neutral productivity
and price $`p = \mu\, c(\mathbf{w})/A`$, to first order,

```math
\Delta \ln \frac{p}{\bar{w}} = \Delta \ln \mu + \sum_i s_i \left( \Delta \ln w_i - \Delta \ln \bar{w} \right) - \Delta \ln A
```

The estimating equation is

```math
y_j = \alpha + \beta\,\frac{\text{CR4}_{j,2002}}{10} + \gamma_{s(j)} + \varepsilon_j, \qquad H_0\!: \beta = 0
```

with $`\gamma_{s(j)}`$ a three-digit subsector effect in the fixed-effects version. The extension estimates

```math
\text{CR4}_{j,2022} = a + \rho\,\text{CR4}_{j,2002} + u_j, \qquad h = \frac{20 \ln 0.5}{\ln \hat{\rho}}
```

## Full test statistics

Slope per 10 points of CR4 (percent a year; margin in points). p-values in parentheses.

| Specification | Price in hours | Real output | TFP | Margin change |
|---|---|---|---|---|
| Unweighted (N = 471) | -0.090 (0.087) | -0.052 (0.712) | 0.121 (0.025) | -0.062 (0.785) |
| Value-added weighted | -0.259 (0.048) | 0.176 (0.059) | 0.169 (0.051) | -0.649 (0.009) |
| Subsector fixed effects | -0.110 (0.017) | -0.284 (0.113) | 0.093 (0.148) | -0.017 (0.941) |
| Without NAICS 334 (N = 441) | -0.044 (0.237) | -0.048 (0.741) | 0.086 (0.082) | -0.022 (0.925) |
| Without 334, weighted | -0.090 (0.076) | 0.141 (0.135) | 0.073 (0.133) | -0.491 (0.029) |
| Winsorized 1%/99% | -0.069 (0.081) | 0.068 (0.412) | 0.125 (0.006) | -0.114 (0.552) |
| Without 324110 and 325110 (N = 469) | -0.081 (0.138) | -0.073 (0.600) | 0.107 (0.055) | -0.117 (0.586) |
| CR8 instead of CR4 | -0.072 (0.139) | -0.041 (0.741) | 0.116 (0.015) | -0.027 (0.898) |
| HHI per 1,000 (N = 443) | -0.434 (0.081) | -0.756 (0.331) | 0.239 (0.339) | -1.381 (0.090) |
| Median regression | 0.000 (0.994) | 0.013 (0.872) | 0.101 (0.002) | -0.061 (0.769) |
| Log average company size | -0.080 (0.328) | 0.590 (< 0.001) | 0.147 (0.022) | 0.265 (0.491) |
| Log company size, subsector FE | -0.210 (0.025) | -0.384 (0.202) | 0.068 (0.549) | 0.193 (0.659) |
| 2007 CR4, 2007-2016 (N = 466) | -0.151 (0.034) | -0.196 (0.392) | 0.140 (0.010) | 0.076 (0.699) |

CR4 ≥ 50 against CR4 < 50 (171 and 300 industries): price in hours -0.98 vs. -0.56% a year (Welch t = -2.29,
p = 0.023); TFP 0.64 vs. 0.18 (t = 2.27, p = 0.024); real output -1.12 vs. -0.96 (p = 0.78); margin change 0.13
vs. 0.60 points (p = 0.63).

Persistence, 2002 to 2022 (N = 256): intercept 8.33, ρ = 0.840 (SE 0.035), t for ρ = 1 equal to -4.53, R² = 0.70,
half-life 79 years (53 to 145 at the ends of the 95% CI for ρ), implied long-run mean 52.0%,
Spearman rank correlation 0.82. Mean CR4 42.0% in 2002 and 43.6% in 2022; standard deviation 20.2 in both years. Of
88 industries with CR4 ≥ 50 in 2002, 67 (76%) remained above 50 in 2022; 21 of 168 below 50 crossed above.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/schumpeter_test.py
python src/temporary_monopoly.py
```

Both scripts run offline from `data/raw/` in under ten seconds each and write every CSV and PNG in `results/`.

## Repository layout

| Path | What it is |
|---|---|
| [src/schumpeter_test.py](src/schumpeter_test.py) | Main test: concentration in 2002 against outcomes to 2016 |
| [src/temporary_monopoly.py](src/temporary_monopoly.py) | Extension: persistence of concentration, 2002 to 2022 |
| [results/FINDINGS.md](results/FINDINGS.md) | Summary and every table |
| `data/raw/` | Census and NBER-CES inputs |

## References

- Arrow, K. J. (1962). Economic welfare and the allocation of resources for invention. In *The Rate and Direction
  of Inventive Activity*, Princeton University Press for NBER.
- Becker, R. A., Gray, W. B. & Marvakov, J. (2021). NBER-CES Manufacturing Industry Database (1958-2018, version
  2021a). National Bureau of Economic Research.
- Nickell, S. J. (1996). Competition and corporate performance. *Journal of Political Economy* 104(4), 724-746.
- Scherer, F. M. (1965). Firm size, market structure, opportunity, and the output of patented inventions.
  *American Economic Review* 55(5), 1097-1125.
- Schumpeter, J. A. (1942). *Capitalism, Socialism and Democracy*. New York: Harper & Brothers.
- US Census Bureau. Economic Census, concentration ratios in manufacturing, 2002, 2007 and 2022.

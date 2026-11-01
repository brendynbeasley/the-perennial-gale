# Schumpeter (1942) on modern data: findings

## In plain English

Joseph Schumpeter argued in 1942 that industries run by a few large companies, not crowds of small ones, are where
goods get cheaper fastest, and that such dominance never lasts long. This repository checks both claims on 471 US
manufacturing industries, using 2002 concentration and outcomes to 2016, and concentration again in 2022.

- **Concentrated industries raised productivity faster.** The most concentrated fifth of industries improved total
  factor productivity by 0.77% a year against 0.12% for the least concentrated fifth. The pattern holds in a median
  regression and in a 2007 to 2016 window, but it weakens when industries are compared only within their own
  subsector or when refining and petrochemicals, whose price indexes break in 2015-2016, are left out.
- **Cheaper goods came mainly from computers and chips.** Computers (Dell, Hewlett-Packard, Apple) became 91%
  cheaper in hours of factory work and semiconductors (Intel, Texas Instruments, Micron) 73% cheaper. Outside that
  subsector, concentrated industries did not cut their prices in hours of labor faster than competitive ones, and
  breakfast cereal (Kellogg, General Mills, Post, Quaker) lost productivity.
- **Margins and output did not move with concentration.** Price-cost margins and real output grew no faster in
  concentrated industries.
- **Concentration lasts.** Of 88 industries where the top four held at least half the market in 2002, 67 still did
  in 2022. Beer, where Anheuser-Busch, Miller and Coors's industry went from 349 to 4,857 companies, is the clearest
  case of Schumpeter's gale; aircraft (Boeing) and breakfast cereal became more concentrated.

A narrative version is in the [README](../README.md); methods are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels.** *CR4* = share of an industry's shipments made by its four largest companies (percent).
*Price in hours of labor* = shipment price index divided by the average hourly pay of a manufacturing production
worker. *g_* = annualized log change, 2002 to 2016, percent a year. *TFP* = five-factor total factor productivity
from NBER-CES. *d_pcm* = change in (value added − payroll) / shipments, percentage points. *vaw* = weighted by
2002 value added. Slopes *b* are per 10 points of CR4 unless the spec says otherwise; standard errors are clustered
by four-digit NAICS group (86 clusters).

## Outcomes by 2002 concentration quintile (results/quintiles.csv)

| Quintile | Industries | CR4 range | Mean CR4 | Value added 2002, $bn | Price in hours, % a year | Output, % a year | TFP, % a year | TFP, median | TFP, vaw | Price in hours, vaw | Margin change, points |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 97 | 2.2-23.8 | 16.7 | 438.1 | -0.55 | -0.66 | 0.12 | 0.03 | 0.08 | -0.48 | 1.00 |
| 2 | 92 | 23.9-36.0 | 29.5 | 350.6 | -0.45 | -1.51 | 0.15 | 0.12 | -1.00 | 0.27 | 1.11 |
| 3 | 95 | 36.1-47.3 | 42.2 | 348.1 | -0.66 | -0.71 | 0.20 | 0.26 | 0.35 | -1.18 | -0.38 |
| 4 | 93 | 47.4-61.8 | 54.5 | 374.1 | -0.90 | -0.97 | 0.49 | 0.47 | 0.88 | -2.01 | 0.16 |
| 5 | 94 | 61.9-99.2 | 75.3 | 365.4 | -1.01 | -1.27 | 0.77 | 0.62 | 0.91 | -1.89 | 0.26 |

The quintile 5 minus quintile 1 TFP gap is 0.646 points a year, or 9.5% cumulated over 14 years.

## Industries with CR4 of 50% or more against the rest (results/headline.csv)

| Measure | High (171) | Low (300) | Gap | Welch t | p | High, vaw | Low, vaw |
|---|---|---|---|---|---|---|---|
| Price in hours of labor, % a year | -0.980 | -0.564 | -0.416 | -2.288 | 0.023 | -2.046 | -0.480 |
| Real output, % a year | -1.122 | -0.961 | -0.161 | -0.283 | 0.777 | 0.211 | -0.395 |
| TFP, % a year | 0.638 | 0.179 | 0.459 | 2.271 | 0.024 | 0.934 | -0.141 |
| Margin change, points | 0.126 | 0.601 | -0.475 | -0.488 | 0.626 | -3.578 | 0.321 |

Other entries in the same file: manufacturing production-worker wage $16.37 an hour in 2002 and $23.28 in 2016;
industries with CR4 ≥ 50 produced 36.4% of 2002 value added; value-weighted change in the price in hours of labor
across all manufacturing -1.050% a year and in TFP 0.251% a year; correlation between TFP growth and the change in
the price in hours of labor -0.601.

## Every regression (results/regressions.csv)

| outcome | spec | window | b | se | p | ci_lo | ci_hi | n |
|---|---|---|---|---|---|---|---|---|
| Price in hours of labor | Unweighted | 2002-2016 | -0.090 | 0.052 | 0.087 | -0.192 | 0.013 | 471 |
| Price in hours of labor | Value-added weighted | 2002-2016 | -0.259 | 0.131 | 0.048 | -0.516 | -0.002 | 471 |
| Price in hours of labor | Subsector fixed effects | 2002-2016 | -0.110 | 0.046 | 0.017 | -0.201 | -0.019 | 471 |
| Price in hours of labor | Without computers and electronics (334) | 2002-2016 | -0.044 | 0.037 | 0.237 | -0.116 | 0.029 | 441 |
| Price in hours of labor | Without 334 and value-added weighted | 2002-2016 | -0.090 | 0.051 | 0.076 | -0.189 | 0.010 | 441 |
| Price in hours of labor | Winsorized 1%/99% | 2002-2016 | -0.069 | 0.040 | 0.081 | -0.147 | 0.009 | 471 |
| Price in hours of labor | Without refining and petrochemicals (324110, 325110) | 2002-2016 | -0.081 | 0.054 | 0.138 | -0.187 | 0.026 | 469 |
| Price in hours of labor | CR8 instead of CR4 | 2002-2016 | -0.072 | 0.048 | 0.139 | -0.167 | 0.023 | 470 |
| Price in hours of labor | HHI per 1000 instead of CR4 | 2002-2016 | -0.434 | 0.249 | 0.081 | -0.921 | 0.054 | 443 |
| Price in hours of labor | Median regression | 2002-2016 | 0.000 | 0.031 | 0.994 | -0.061 | 0.061 | 471 |
| Price in hours of labor | Log average company size | 2002-2016 | -0.080 | 0.082 | 0.328 | -0.239 | 0.080 | 471 |
| Price in hours of labor | Log average company size with subsector FE | 2002-2016 | -0.210 | 0.094 | 0.025 | -0.395 | -0.026 | 471 |
| Price in hours of labor | 2007 CR4 with 2007-2016 growth | 2007-2016 | -0.151 | 0.071 | 0.034 | -0.291 | -0.011 | 466 |
| Real output | Unweighted | 2002-2016 | -0.052 | 0.141 | 0.712 | -0.328 | 0.224 | 471 |
| Real output | Value-added weighted | 2002-2016 | 0.176 | 0.093 | 0.059 | -0.007 | 0.360 | 471 |
| Real output | Subsector fixed effects | 2002-2016 | -0.284 | 0.179 | 0.113 | -0.635 | 0.067 | 471 |
| Real output | Without computers and electronics (334) | 2002-2016 | -0.048 | 0.145 | 0.741 | -0.333 | 0.237 | 441 |
| Real output | Without 334 and value-added weighted | 2002-2016 | 0.141 | 0.094 | 0.135 | -0.044 | 0.325 | 441 |
| Real output | Winsorized 1%/99% | 2002-2016 | 0.068 | 0.083 | 0.412 | -0.095 | 0.232 | 471 |
| Real output | Without refining and petrochemicals (324110, 325110) | 2002-2016 | -0.073 | 0.140 | 0.600 | -0.347 | 0.200 | 469 |
| Real output | CR8 instead of CR4 | 2002-2016 | -0.041 | 0.124 | 0.741 | -0.285 | 0.203 | 470 |
| Real output | HHI per 1000 instead of CR4 | 2002-2016 | -0.756 | 0.778 | 0.331 | -2.282 | 0.769 | 443 |
| Real output | Median regression | 2002-2016 | 0.013 | 0.082 | 0.872 | -0.148 | 0.174 | 471 |
| Real output | Log average company size | 2002-2016 | 0.590 | 0.137 | 0.000 | 0.321 | 0.859 | 471 |
| Real output | Log average company size with subsector FE | 2002-2016 | -0.384 | 0.301 | 0.202 | -0.974 | 0.205 | 471 |
| Real output | 2007 CR4 with 2007-2016 growth | 2007-2016 | -0.196 | 0.229 | 0.393 | -0.645 | 0.253 | 466 |
| Total factor productivity | Unweighted | 2002-2016 | 0.121 | 0.054 | 0.025 | 0.015 | 0.226 | 471 |
| Total factor productivity | Value-added weighted | 2002-2016 | 0.169 | 0.087 | 0.051 | -0.001 | 0.338 | 471 |
| Total factor productivity | Subsector fixed effects | 2002-2016 | 0.093 | 0.064 | 0.147 | -0.033 | 0.218 | 471 |
| Total factor productivity | Without computers and electronics (334) | 2002-2016 | 0.086 | 0.050 | 0.082 | -0.011 | 0.183 | 441 |
| Total factor productivity | Without 334 and value-added weighted | 2002-2016 | 0.073 | 0.048 | 0.133 | -0.022 | 0.168 | 441 |
| Total factor productivity | Winsorized 1%/99% | 2002-2016 | 0.125 | 0.046 | 0.006 | 0.035 | 0.215 | 471 |
| Total factor productivity | Without refining and petrochemicals (324110, 325110) | 2002-2016 | 0.107 | 0.056 | 0.055 | -0.002 | 0.217 | 469 |
| Total factor productivity | CR8 instead of CR4 | 2002-2016 | 0.116 | 0.048 | 0.015 | 0.022 | 0.209 | 470 |
| Total factor productivity | HHI per 1000 instead of CR4 | 2002-2016 | 0.239 | 0.250 | 0.339 | -0.251 | 0.730 | 443 |
| Total factor productivity | Median regression | 2002-2016 | 0.101 | 0.033 | 0.002 | 0.037 | 0.166 | 471 |
| Total factor productivity | Log average company size | 2002-2016 | 0.147 | 0.064 | 0.022 | 0.021 | 0.273 | 471 |
| Total factor productivity | Log average company size with subsector FE | 2002-2016 | 0.068 | 0.113 | 0.549 | -0.154 | 0.289 | 471 |
| Total factor productivity | 2007 CR4 with 2007-2016 growth | 2007-2016 | 0.140 | 0.055 | 0.011 | 0.033 | 0.248 | 466 |
| Price-cost margin change (points) | Unweighted | 2002-2016 | -0.062 | 0.227 | 0.785 | -0.506 | 0.382 | 471 |
| Price-cost margin change (points) | Value-added weighted | 2002-2016 | -0.649 | 0.250 | 0.009 | -1.138 | -0.159 | 471 |
| Price-cost margin change (points) | Subsector fixed effects | 2002-2016 | -0.017 | 0.226 | 0.941 | -0.459 | 0.425 | 471 |
| Price-cost margin change (points) | Without computers and electronics (334) | 2002-2016 | -0.022 | 0.231 | 0.925 | -0.475 | 0.431 | 441 |
| Price-cost margin change (points) | Without 334 and value-added weighted | 2002-2016 | -0.491 | 0.225 | 0.029 | -0.931 | -0.050 | 441 |
| Price-cost margin change (points) | Winsorized 1%/99% | 2002-2016 | -0.114 | 0.192 | 0.552 | -0.491 | 0.262 | 471 |
| Price-cost margin change (points) | Without refining and petrochemicals (324110, 325110) | 2002-2016 | -0.117 | 0.215 | 0.586 | -0.538 | 0.304 | 469 |
| Price-cost margin change (points) | CR8 instead of CR4 | 2002-2016 | -0.027 | 0.206 | 0.898 | -0.431 | 0.378 | 470 |
| Price-cost margin change (points) | HHI per 1000 instead of CR4 | 2002-2016 | -1.381 | 0.816 | 0.090 | -2.980 | 0.218 | 443 |
| Price-cost margin change (points) | Median regression | 2002-2016 | -0.061 | 0.206 | 0.769 | -0.466 | 0.345 | 471 |
| Price-cost margin change (points) | Log average company size | 2002-2016 | 0.265 | 0.385 | 0.491 | -0.489 | 1.020 | 471 |
| Price-cost margin change (points) | Log average company size with subsector FE | 2002-2016 | 0.193 | 0.438 | 0.659 | -0.665 | 1.051 | 471 |
| Price-cost margin change (points) | 2007 CR4 with 2007-2016 growth | 2007-2016 | 0.076 | 0.197 | 0.699 | -0.309 | 0.461 | 466 |

## Named industries (results/named_industries.csv)

Leaders are well-known producers in 2002, not Census data. Changes are 2002 to 2016.

| NAICS | Industry | Leaders | Companies 2002 | CR4 2002 | Shipments 2002, $bn | Price in hours, % change | TFP, % change | Real output, % change | Margin 2002 | Margin change |
|---|---|---|---|---|---|---|---|---|---|---|
| 312221 | Cigarettes | Philip Morris (Altria), R.J. Reynolds | 15 | 95.3 | 34.80 | -19.34 | 8.72 | -14.11 | 85.11 | -5.96 |
| 312120 | Breweries | Anheuser-Busch, Miller, Coors | 349 | 90.8 | 17.86 | 1.42 | 19.40 | 23.03 | 53.24 | 5.75 |
| 331312 | Primary aluminum | Alcoa, Century Aluminum | 26 | 85.3 | 4.75 | -34.77 | 49.46 | -30.42 | 22.92 | 6.76 |
| 336411 | Aircraft | Boeing | 184 | 80.7 | 64.31 | -4.43 | 15.30 | 47.24 | 29.45 | 2.00 |
| 311230 | Breakfast cereal | Kellogg, General Mills, Post, Quaker | 45 | 78.4 | 9.10 | -5.61 | -28.05 | -21.31 | 66.78 | -33.29 |
| 334111 | Electronic computers | Dell, Hewlett-Packard, Apple | 465 | 75.5 | 47.73 | -90.83 | 276.49 | 60.92 | 37.03 | -7.57 |
| 336111 | Automobiles | General Motors, Ford, DaimlerChrysler, Toyota | 164 | 75.5 | 88.13 | -23.27 | -3.01 | 31.37 | 26.13 | -10.32 |
| 334413 | Semiconductors | Intel, Texas Instruments, Micron | 904 | 56.5 | 61.43 | -73.29 | 98.97 | 94.47 | 58.72 | -21.64 |
| 335221 | Household cooking appliances | Whirlpool, GE, Electrolux | 92 | 48.3 | 4.33 | -20.09 | 44.56 | 1.31 | 25.92 | 5.85 |
| 331111 | Iron and steel mills | U.S. Steel, Nucor | 285 | 44.4 | 47.04 | -8.26 | 34.50 | 27.19 | 25.53 | 2.24 |
| 324110 | Petroleum refineries | ExxonMobil, ConocoPhillips, BP | 88 | 41.2 | 193.53 | -50.58 | 13.23 | 183.76 | 12.10 | 3.56 |
| 325412 | Pharmaceuticals | Pfizer, Merck, Johnson & Johnson | 731 | 36.0 | 114.67 | 45.61 | -43.90 | -30.00 | 64.58 | -0.57 |
| 321113 | Sawmills | Weyerhaeuser and thousands of small mills | 3,462 | 17.5 | 21.39 | -23.73 | 38.18 | -1.49 | 17.24 | 11.98 |
| 323110 | Commercial printing | Thousands of print shops | 14,970 | 12.4 | 50.52 | -23.98 | 12.42 | -26.96 | 33.07 | -0.40 |
| 327320 | Ready-mix concrete | Thousands of local producers | 2,614 | 11.1 | 21.62 | 16.95 | -9.69 | -16.88 | 30.81 | 4.93 |
| 332710 | Machine shops | Thousands of machine shops | 22,180 | 2.2 | 26.27 | -6.89 | -4.49 | 2.80 | 33.70 | -1.81 |

The refinery figures are unreliable as a 2002 to 2016 comparison. The NBER-CES shipment price index for NAICS
324110 drops sharply in 2015 and 2016, by much more than the industry's materials price index, which inflates
measured real output and TFP. Petrochemicals (325110, CR4 84.7%, TFP growth 7.67% a year in results/industries.csv)
shows the same break. Both stay in the main sample; the "Without refining and petrochemicals" rows above drop them,
and the median and winsorized regressions limit their influence.

## Extension: persistence of concentration, 2002 to 2022 (results/persistence.csv)

256 industries whose six-digit definition is unchanged in every NAICS revision from 2002 to 2022.

| Statistic | Value |
|---|---|
| Persistence slope ρ (SE) | 0.840 (0.035) |
| 95% CI | [0.770, 0.909] |
| t for ρ = 1 | -4.527 |
| Intercept | 8.331 |
| R² | 0.700 |
| Annual persistence ρ^(1/20) | 0.991 |
| Half-life of a departure from the long-run mean | 79.3 years (53.1 to 145.5 at the ends of the 95% CI) |
| Implied long-run mean CR4 | 52.0% |
| Mean CR4, 2002 and 2022 | 42.0%, 43.6% |
| Standard deviation, 2002 and 2022 | 20.2, 20.2 |
| Pearson and Spearman correlation | 0.837, 0.822 |
| CR4 ≥ 50 in 2002 | 88 industries; 67 (76.1%) still ≥ 50 in 2022; mean change -1.98 points |
| CR4 < 50 in 2002 | 168 industries; 21 crossed 50 by 2022; mean change +3.48 points |
| Mean absolute change | 8.95 points |
| Share moving 10 points or more | 35.2% |

## Movement between concentration bands (results/persistence_transitions.csv)

Rows are 2002 bands, columns 2022 bands; cells count industries.

| 2002 \ 2022 | Under 25% | 25-50% | 50-75% | 75% or more |
|---|---|---|---|---|
| Under 25% | 39 | 24 | 0 | 0 |
| 25-50% | 7 | 77 | 21 | 0 |
| 50-75% | 2 | 19 | 38 | 12 |
| 75% or more | 0 | 0 | 7 | 10 |

## Named industries, 2002 and 2022 (results/persistence_named.csv)

| NAICS | Industry | Leaders in 2002 | CR4 2002 | CR4 2022 | Change | Companies 2002 | Companies 2022 |
|---|---|---|---|---|---|---|---|
| 312120 | Breweries | Anheuser-Busch, Miller, Coors | 90.8 | 63.6 | -27.2 | 349 | 4,857 |
| 336411 | Aircraft | Boeing | 80.7 | 83.5 | +2.8 | 184 | 234 |
| 311230 | Breakfast cereal | Kellogg, General Mills, Post, Quaker | 78.4 | 86.6 | +8.2 | 45 | 77 |
| 334111 | Electronic computers | Dell, Hewlett-Packard, Apple | 75.5 | 60.5 | -15.0 | 465 | 148 |
| 334413 | Semiconductors | Intel, Texas Instruments, Micron | 56.5 | 48.0 | -8.5 | 904 | 675 |
| 324110 | Petroleum refineries | ExxonMobil, ConocoPhillips, BP | 41.2 | 52.2 | +11.0 | 88 | 50 |
| 325412 | Pharmaceuticals | Pfizer, Merck, Johnson & Johnson | 36.0 | 39.8 | +3.8 | 731 | 1,131 |
| 327320 | Ready-mix concrete | Thousands of local producers | 11.1 | 15.0 | +3.9 | 2,614 | 1,994 |

Cigarettes, primary aluminum and steel mills are absent because their NAICS definitions changed in 2012.

## Other files

- `results/industries.csv`: one row per industry (471) with concentration, price indexes, TFP, margins and every
  outcome.
- `results/persistence_industries.csv`: one row per industry in the persistence sample (256).
- `results/manufacturing_wage.csv`: the production-worker hourly wage for every year, 1958 to 2018.
- Figures: `results/tfp_by_quintile.png`, `results/price_in_hours.png`, `results/persistence.png`.

# Methods review: Schumpeter (1942)

- **Paper:** Joseph A. Schumpeter, *Capitalism, Socialism and Democracy*. New York: Harper & Brothers, 1942.
  Chapters 7 ("The Process of Creative Destruction") and 8 ("Monopolistic Practices"), with chapter 5 ("The Rate
  of Increase of Total Output") for the growth figures the argument builds on.
- **Statistical focus:** the claim that the largest declines in prices measured in hours of labor came from
  industries dominated by large concerns, supported by the Aluminum Company of America example (price down to about
  12% of its 1890 level by 1929, about 8.8% in real terms, output up from 30 to 103,400 metric tons), and the claim
  that monopoly positions are temporary.
- **Review standard:** for a book-length argument without formal estimation, the internal consistency of the
  argument, whether its assumptions are stated, whether its evidence is sourced and reproducible, and whether its
  predictions are testable. Where figures are given, the standard reporting of sources, definitions, sample
  construction and uncertainty.
- **What was read:** the full text of the Harper & Brothers second edition, as scanned in the Internet Archive's
  Digital Library of India collection (item `in.ernet.dli.2015.190072`). Chapters 5, 7 and 8 were read in full;
  the rest of the book was consulted only for its table of contents. Page numbers below refer to that edition, and
  I did not compare them with a first-edition copy.

## Methods summary

**Research design.** An interpretive historical and theoretical argument. Schumpeter contrasts the static theory
of monopoly and imperfect competition with an evolutionary view in which new goods, methods and forms of
organization ("creative destruction," p. 83) are the competition that matters. Evidence enters as illustrations,
not as a designed comparison.

**Sampling strategy.** Not applicable in the usual sense. Examples are chosen by the author to illustrate the
argument: the Aluminum Company of America, the automobile industry, rayon, agricultural machinery, retail trade.
There is no stated rule for which industries are included, so the examples cannot be read as a sample.

**Sample size.** Not applicable. The one quantitative case is a single firm (Alcoa) over 1890 to 1929. The
proposed systematic test, the list of items in a worker's budget priced in hours of labor from 1899 on (pp. 81-82),
is described but not carried out in the text.

**Inclusion and exclusion criteria.** Not stated. The book sets aside cartels that do not improve methods of
production (p. 102) and "fringe-end cases" of small-scale retail (p. 85) as exceptions, which narrows the claim to
large-scale manufacturing.

**Independent and dependent variables.** Implicitly, the independent variable is the presence of large-scale
firms or "monopoloid" structure, and the dependent variables are long-run output growth and prices measured in
hours of labor. Neither is defined operationally. "Large concern" is not given a size threshold, and "monopoly" is
used in both a technical and a popular sense (footnote on Alcoa, p. 101).

**Statistical methods.** None beyond growth arithmetic. Chapter 5 computes average annual growth from the
Day-Persons index of production and compounds a 2% rate over fifty years (pp. 64-65).

**Reported effect sizes.** Ratios and growth rates in the extraction table below. None is a comparison between
concentrated and unconcentrated industries; the Alcoa figures describe one firm's price and output path without a
counterfactual.

**Confidence intervals.** None reported. Not expected for the material presented, but the absence means the
precision of the Day-Persons growth rates and the Alcoa price series cannot be judged.

**p-values.** Not applicable; no hypothesis tests are reported.

**Missing data treatment.** Not discussed. The Alcoa price series is deflated by the BLS wholesale price index,
named in the footnote, but the underlying price and output sources are not cited.

**Stated limitations.** Schumpeter states that the argument over output growth must be judged over decades
(p. 83), that restrictive practices and the classical monopoly result apply where monopolization brings no
improvement in methods (p. 102), and that genuine monopoly positions are more common in the short run (p. 102). He
also writes that the 1.7% allowance he subtracts for durable equipment in chapter 5 is a judgment ("I believe that
an allowance of 1.7 per cent is ample," p. 64).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| US total production growth, 1870-1930 | 3.7% a year | Ch. 5, p. 64, Day-Persons index | Long-run growth of an index of physical production | Any link between growth and firm size or market structure |
| US manufactures growth, 1870-1930 | 4.3% a year | Ch. 5, p. 64 | Growth of manufacturing output on the same index | Which industries or firm types produced the growth |
| "Available output" growth | 2% a year after a 1.7-point allowance for durable equipment | Ch. 5, p. 64 | Author's adjusted rate of growth of output available for consumption | The allowance is a stated judgment, not an estimate |
| Projected output multiple, 1928-1978 | About 2.7 (2.6916) times the 1928 level | Ch. 5, p. 65 | 2% compounded for fifty years | A forecast; it assumes the past rate continues |
| Alcoa price of basic product, 1890-1929 | Fell to about 12% of the 1890 level | Ch. 8, footnote 20, p. 101 | Nominal price decline for one firm's product | That the decline was caused by Alcoa's market position rather than technology or scale available to any producer |
| Alcoa price, deflated | About 8.8% of the 1890 level, BLS wholesale price index | Ch. 8, footnote 20, p. 101 | Real price decline | A comparison with competitive industries over the same years |
| Alcoa output, 1890-1929 | 30 to 103,400 metric tons | Ch. 8, footnote 20, p. 101 | Growth of physical output | Welfare relative to a counterfactual with more sellers; the footnote notes patent protection ended in 1909 |
| Automobile industry concentration | Three concerns "over 80 per cent of total sales" | Ch. 8, footnote, p. 90 | Concentration after the shakeout that ended around 1925 | Whether the three firms' conduct was competitive; the source for the share is not given |

## Interpretation notes

- The book's strongest empirical claim, that progress "leads ... to the doors of the large concerns" (p. 82), is
  stated as the outcome of an exercise the reader is invited to do. No list of goods, prices or wage series is
  provided, so the claim cannot be checked from the book alone.
- The Alcoa case is consistent with the argument but is a single example selected by the author. A falling price
  and rising output under a dominant seller are also what a static monopoly model predicts if costs fall fast
  enough, so the example does not by itself distinguish Schumpeter's view from the textbook one.
- The argument is explicitly dynamic. It concedes that monopoly may restrict output at a point in time and claims
  that the long-run rate of improvement more than compensates. A fair test therefore compares rates of change over
  long windows, which is what this repository does with 2002 to 2016 outcomes.
- The claim that positions are temporary is qualitative. The book gives no rate at which positions erode, so the
  persistence estimate here (a half-life near 79 years for concentration) cannot be said to confirm or contradict a
  number in the book; it gives a magnitude the book leaves open.
- Reporting issues, kept separate from analytical ones: sources for the Alcoa price and output series and for the
  automobile share are not cited, and the Day-Persons index is named without a reference to its construction. I
  found no published correction of these figures and do not suggest they are wrong.

## Unanswered questions

- Which goods, in which years, did Schumpeter have in mind for the hours-of-labor comparison, and would a
  systematic list from 1899 to 1940 have favored large-firm industries?
- How much of Alcoa's price decline came from the electrolytic process and cheap hydroelectric power, which a
  competitive industry could also have used, rather than from Alcoa's size or market position?
- What size or market share makes a firm a "large concern" in the sense the argument needs?
- How fast must positions erode for the dynamic argument to outweigh static losses from restricted output?

## Items requiring expert verification

- Whether the pagination of the second edition used here matches the 1942 first edition for chapters 5 to 8.
- The original sources and accuracy of the Alcoa price and output figures, and whether "metric tons" refers to
  primary aluminum production in the United States or Alcoa's own output.
- The construction of the Day-Persons index and whether its 1870 to 1930 growth rate has been revised by later
  historical series.
- Whether later scholarship (for example on the 1945 *United States v. Aluminum Co. of America* decision) gives a
  different account of Alcoa's pricing over the same period.

The modern rerun in this repository is not a reproduction of anything in the book, since the book reports no
dataset. It applies Schumpeter's own yardstick, prices in hours of labor, together with productivity and output, to
471 US manufacturing industries from 2002 to 2016, and adds a persistence test for his claim that positions erode.

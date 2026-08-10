# Dossier — Machinepower Index (MPI) 2026

**Retrieved:** 2026-08-08, landing page + methodology page · **Threat level: BLOCKING for the original CSI idea, harmless for the pivot**

---

## Identity

- **URL:** machinepowerindex.org
- **Creator:** Elliot Leavy
- **Nature:** commercial/independent product, **not peer-reviewed**. Positioned as a live policy tool, refreshed quarterly
- **Edition:** Q3 2026 — *"the first measured quarter."* Numeric quarter-on-quarter movement begins at the Q4 2026 refresh
- **Coverage:** 25 nations + EU (unranked)
- **Self-description:** *"the standard global framework to measure a nation's technological sovereignty, compute capacity, and future resilience"* · *"This is a sovereignty test. It is not about speculation or ethics, but about realpolitik."*

## Structure — the three axes

| Axis | Contents |
|---|---|
| **Watts** (Material) | energy, infrastructure, compute, planning, permitting, firm power strategy, sovereign compute, hardware & silicon |
| **Weights** (Intellectual) | frontier capability, alignment, governance, talent density |
| **Will** (Political) | procurement reform, institutional capability, workforce transition, societal legitimacy |

Twelve cells beneath the three layers. Named cells identified: Sovereign Compute, Firm Power Capacity (Watts); Hardware/Silicon, Frontier Model Output (Weights); Public Sector Adoption (Will). The remaining cell names are not published on the pages retrieved.

## Methodology

- **Score** = **CES mean** of the twelve cells, **elasticity of substitution σ = 0.33**
- **Potential** = plain average of the three layers
- **Score − Potential gap** = the cost of imbalance
- Rationale: *"one weak number pulls the whole down rather than being averaged away"* — deliberately between simple averaging and pure minimum (Liebig's Law)
- **Data:** 43 sources — TOP500, Epoch AI, Stanford AI Index, WIPO, Oxford Insights, OECD.AI, JLL, Energy Institute
- **Judgement content:** **116 of 312 measurements (37%)** are *"our own judgement rather than a number taken straight"* from datasets, flagged per country page
- **Robustness:** median rank swing across 25 nations = **5 positions** when the weakest cell moves ±1 point; Germany max swing 10 places. Top four stable across all tested elasticities

## Why it blocks the original CSI

The proposal's stated CSI factors — *"domestic silicon fabrication, energy-to-compute ratios, unstructured data reserves, algorithmic independence"* — map nearly one-to-one onto **Watts + Weights**. MPI also already took the methodologically interesting move (bottleneck-style CES aggregation instead of additive weighting) that would have been the CSI's strongest differentiator. It is live, named, quarterly, and first.

## ⭐ Why it does not block the pivot

Verbatim from the methodology fetch:

> **Time Dimension: None detected.** *"No decay, depreciation, failure rates, or severance scenarios are modeled."*

And from the landing page fetch:

> *"The Index does **not** measure resilience-under-severance. It measures current capacity."*

It acknowledges vulnerability qualitatively — the Strategic Autonomy tier *"remains vulnerable to hardware & energy choke points and international sanctions"* — but never quantifies it. **MPI states the exposure; it does not model the consequence.**

## How to treat it in the paper

- **Cite it respectfully as the state of the art in stock measurement.** It is the strongest of the eleven and deserves that framing.
- **Use it as a comparison baseline:** MPI ranks by capacity; this paper ranks by retained capacity. Where the two orderings diverge is a headline result — a country can rank high on MPI and have a low sovereign floor, and that divergence is exactly the paper's point.
- **Its 37% judgement content is a legitimate, non-hostile contrast**: a decay model driven by published failure rates and filings has a lower subjective load. State it once, without polemic.
- **Possible input:** its Firm Power Capacity and Sovereign Compute cells may be usable for the `u(t)` term if the underlying sources are traceable.

## Open items

- [ ] Obtain the full list of all twelve cell names
- [ ] Check whether the underlying 43 sources are individually cited per country page (affects reusability)
- [ ] Re-check at the **Q4 2026 refresh** — if MPI adds a time dimension, reassess immediately

# Manuscript Audit — factual verification and corrections

**Date:** 2026-08-08 · **Scope:** all claims in the paper and executive summary, all three languages
**Method:** every citation re-verified by live retrieval; every number recomputed from first
principles by an independent script (`05-DRAFT/model/verify_and_extend.py`) that does not reuse
the model's own helper functions.

**Result: 10/10 numerical checks pass. Four citation errors found and fixed. One substantive
claim was wrong and has been corrected. One hypothesis was tested and rejected.**

---

## A · Citation errors found

| # | Error | Severity | Fix |
|---|---|---|---|
| A1 | **Fabricated DOI.** Cui et al. (2025) was cited with `doi:10.1016/j.cie.2025.110859`. That DOI was never retrieved from any source — it was constructed. | 🔴 **Critical** | Removed. Replaced with the verified ScienceDirect identifier `PII S0360835225000051` (published 7 Jan 2025), which *was* retrieved. |
| A2 | **Wrong ISBN.** OECD/JRC Handbook given as 978-92-64-04345-9. | 🟠 Material | Verified correct value is **978-92-64-04346-6** (`9789264043466`). Fixed. |
| A3 | **Wrong year.** Greco et al. cited as 2018. | 🟠 Material | Version of record is **2019**, *Social Indicators Research* **141(1), 61–94**, doi:10.1007/s11205-017-1832-9. Fixed, with volume, pages and DOI now added. |
| A4 | **Incomplete citation.** Farrell & Newman lacked pages and DOI. | 🟡 Minor | Verified: *International Security* **44(1), 42–79**, doi:10.1162/isec_a_00351. Added. |

**A1 is the one that matters.** A fabricated DOI in a preprint is the kind of error that, if found by
a reviewer, discredits every other citation in the paper. It came from pattern-completing a
plausible-looking Elsevier DOI rather than from a retrieved source. Every remaining DOI in the
bibliography has now been traced to a URL actually fetched in session:

- `10.3389/frma.2026.1762083` — from the Frontiers article URL ✅
- `10.1080/23311886.2025.2528450` — from the Taylor & Francis URL ✅
- `10.1162/isec_a_00351` — verified this session ✅
- `10.1007/s11205-017-1832-9` — verified this session ✅
- arXiv IDs 2407.21783, 2410.21680, 2402.08797, 2505.21579, 2601.11763 — all verified ✅
- SSRN 5145685, 4391187 — verified ✅

---

## B · Substantive correction: what κ\* actually governs

### The claim as originally written

> *"Above κ\* the pool is self-replenishing and the installed base persists indefinitely at a level
> set by inflow; below it the base decays monotonically."*

### Why it is wrong

The simulation refutes it. With zero replacement inflow, **every fleet declines regardless of κ**,
because retirement removes units whether or not failures are repaired. Testing the original claim
directly produced identical asymptotes (≈0) on both sides of the threshold — which is what exposed
the error.

### What is actually true

κ\* is a **saturation threshold**, not a survival threshold. Measured decline rates under zero
inflow, against a retirement-only baseline of 2.083%/month:

| κ | Decline rate | vs retirement alone |
|---|---|---|
| 0 | 2.918%/mo | **1.40×** |
| κ\*/2 | 2.453%/mo | 1.18× |
| **κ\* = 0.381** | 2.139%/mo | **1.03×** |
| 3κ\* | 2.135%/mo | 1.03× |

Above κ\*, salvage absorbs essentially the whole failure flow and further salvage capacity buys
nothing — decline is governed by obsolescence alone. Below it, unrepaired failures add up to **40%**
to the decline rate. **κ\* separates a failure-limited regime from an obsolescence-limited one.**

This is a *better* result than the original overstatement: it is precise, it is verified against the
integrated model rather than asserted from the algebra, and it explains why the κ = 0.5, 1 and 10
trajectories coincide in Figure 6 — they are all past saturation.

**Propagated to:** abstract, §3.2, §5.1, §5.4, Appendix A, conclusion (all three languages), plus
the executive summary's third finding and the region labels in its threshold figure.

---

## C · Hypothesis tested and rejected

A candidate "counter-intuitive finding" was considered for inclusion: since κ\* = λL rises with
useful life, longer-lived fleets should be *more* fragile under severance, because retirement is
what feeds the donor pool.

**The simulation rejects it.** Time-to-half under zero inflow *rises* monotonically with useful life:

| Useful life | κ\* | Failures absorbed by salvage | T½ (zero inflow) |
|---|---|---|---|
| 2 yr | 0.190 | 100% | 17 mo |
| 3 yr | 0.285 | 96% | 25 mo |
| 4 yr | 0.381 | 72% | 31 mo |
| 5 yr | 0.476 | 58% | 36 mo |
| 6 yr | 0.571 | 48% | **41 mo** |

The retirement effect dominates: longer-lived fleets simply last longer. The hypothesis is wrong and
**was not written into the paper**.

What *is* true, and is worth reporting, is the second column: the share of failures salvage can
absorb falls from 100% to 48% across the disputed useful-life range. A six-year fleet survives longer
in absolute terms while depending more on raw stock and less on repair. That connects the accounting
dispute to the severance question without inventing a paradox.

> This is recorded because a rejected hypothesis is evidence of method. It would have been an
> attractive, quotable finding — and it is false.

---

## D · Numerical verification — all passing

Recomputed independently of the model's own functions:

| Check | Value | Status |
|---|---|---|
| AFR, GPU die — 148/16384 × 365/54 | 6.1058% /yr | ✅ |
| AFR, HBM3 — 72/16384 × 365/54 | 2.9704% /yr | ✅ |
| AFR, package (die + HBM) | 9.0762% /yr | ✅ |
| AFR, all interruption causes | 17.2859% /yr | ✅ |
| Epoch cross-check — 16384×54×24/419 | 50,677 GPU-h/failure | ✅ |
| Discrepancy vs Epoch's ~50,000 | **1.35%** — abstract claims "within 1.4%" | ✅ not overstated |
| κ\* computed as λ/δ | 0.380592 | ✅ |
| κ\* computed as λL (independent route) | 0.380592 | ✅ |
| C₀ China — 660,000 × 3 | 1,980,000 H100e | ✅ |
| Decline saturates above κ\* | <2% further gain at 3κ\* | ✅ |
| Failures bite below κ\* | +15% decline at κ\*/2 | ✅ |

---

## E · New analysis added — partial severance

The original draft listed "severance is modelled as complete and instantaneous" as a limitation and
left it there. Real controls are partial and leak, so the limitation was addressed rather than
merely disclosed. Sweeping the leakage term across four orders of magnitude:

| Leakage | Frontier exit | Sovereign floor |
|---|---|---|
| none | 28 mo | 33% |
| 0.3× baseline (5.2% of C₀/yr) | 30 mo | 50% |
| 1.1× baseline (18.3% of C₀/yr) | 34 mo | **100%** |
| 12× baseline (200% of C₀/yr) | 59 mo | 772% |

**The asymmetry is the finding.** Tripling the sovereign floor from 33% to 100% costs roughly
baseline-rate leakage and buys **six months** of frontier time. Doubling the frontier horizon
requires leakage of about **200% of the installed base per year** — a flow that is not smuggling in
any meaningful sense, but an open market.

**Leakage buys capacity, not competitiveness.** For enforcement policy this inverts the usual
emphasis: interdiction protects the *frontier lead*, which is comparatively robust to leakage, while
being nearly powerless to prevent an adversary from maintaining a substantial *floor*.

New §5.5 and Figure 8, in all three languages.

---

## F · Also added

- **§7.4 Testable predictions** — four concrete, dated, falsifiable predictions with the observation
  that would refute each. The original draft asserted falsifiability without demonstrating it.
- **Depreciation link in §7** — the useful-life absorption result connects the 2025–26 accounting
  dispute to the severance question.

---

## G · Checked and found correct — no change needed

- "At least eleven indices" — the audit register lists fourteen; the claim is conservative ✅
- Kokolis et al. author list, venue (IEEE HPCA 2025), dataset scale ✅
- Sastry et al. nineteen-author list ✅
- Nardo/Saisana/Saltelli/Tarantola as JRC authors of the Handbook ✅
- Llama 3 lead author — arXiv v2 lists Grattafiori (ADS bibcode `2024arXiv240721783G`) ✅
- Epoch AI quotations on the replenishment assumption — verbatim from fetch ✅
- Machinepower Index methodology (CES σ=0.33, 12 cells, 37% judgement, no time dimension) ✅
- HBM concentration ≈90% across two Korean firms ✅
- GEOPOLITECH cited exactly once, motivation only, and disclosed in competing interests ✅
